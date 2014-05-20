/// <reference path="jquery.d.ts" />
/// <reference path="handlebars.d.ts" />

var StripImage = (function () {
    function StripImage(image) {
        this.src = image.image;
    }
    return StripImage;
})();

var Strip = (function () {
    function Strip(strip, template) {
        this.template = template;
        this.images = new Array();
        for (var i = 0; i < strip.images.length; i++) {
            this.images.push(new StripImage(strip.images[i]));
        }
    }
    Strip.prototype.render = function () {
        return this.template(this);
    };

    Strip.prototype.reset = function () {
    };
    return Strip;
})();

var ComicsManager = (function () {
    function ComicsManager($target, endPoint) {
        this.endPoint = endPoint;
        this.$target = $target;
        this.templates = {};
        this.strips = new Array();

        $(document).keypress(this.handleKeyDownEvent);

        this.getStripsFromServer();
    }
    ComicsManager.prototype.handleKeyDownEvent = function (e) {
        console.log("key pressed");
    };

    ComicsManager.prototype.getStripsFromServer = function () {
        var _this = this;
        var stripApiUrl = this.endPoint + "api/v1/strips/";
        $.ajax({
            url: stripApiUrl,
            method: 'get',
            success: function (result, status, xhr) {
                for (var i = 0; i < result.length; i++) {
                    var stripObj = result[i];
                    var templateName = stripObj.template;

                    if (!_this.templates.hasOwnProperty(templateName)) {
                        /* this method is executed synchronously, as the entire
                        callback is async anyway. */
                        _this.compileTemplate(templateName);
                    }
                    var template = _this.templates[templateName];
                    var strip = new Strip(stripObj, template);

                    _this.$target.append(strip.render());
                    _this.strips.push(strip);
                }
            }
        });
    };

    ComicsManager.prototype.advanceToNextStrip = function () {
        if (this.currentStripIdx == this.strips.length - 1) {
            return;
        }

        this.advanceToStrip(this.strips[this.currentStripIdx + 1]);
    };

    ComicsManager.prototype.advanceToStrip = function (strip) {
        this.strips[this.currentStripIdx].reset();
    };

    ComicsManager.prototype.compileTemplate = function (template) {
        var _this = this;
        var templatesBaseDir = this.endPoint + "static/templates/";
        var templateUrl = templatesBaseDir + template + ".handlebars";
        $.ajax({
            url: templateUrl,
            method: 'get',
            async: false,
            success: function (args) {
                _this.templates[template] = Handlebars.compile(args);
            }
        });
    };
    return ComicsManager;
})();

(function ($, endpoint) {
    $(document).ready(function () {
        var manager = new ComicsManager($("#strips-list"), endpoint);
    });
})(jQuery, SERVER_ENDPOINT);
