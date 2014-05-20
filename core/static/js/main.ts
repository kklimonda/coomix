/// <reference path="jquery.d.ts" />
/// <reference path="handlebars.d.ts" />
declare var SERVER_ENDPOINT: string;

class StripImage {
    src: string;

    constructor(image) {
       this.src = image.image; 
    }
}

class Strip {
    images: StripImage[];
    template: HandlebarsTemplateDelegate;

    constructor(strip, template: HandlebarsTemplateDelegate) {
        this.template = template;
        this.images = new Array<StripImage>();
        for (var i = 0; i < strip.images.length; i++) {
            this.images.push(new StripImage(strip.images[i]));
        }
    }

    render() : string {
        return this.template(this);
    }

    reset() : void {

    }
} 


class ComicsManager {
    /* cache of the compiled templates for strips */
    templates: { [index: string]: HandlebarsTemplateDelegate };
    endPoint: string;
    strips: Strip[];
    $target: JQuery;
    currentStripIdx: number;

    constructor($target: JQuery, endPoint: string) {
        this.endPoint = endPoint;
        this.$target = $target;
        this.templates = {};
        this.strips = new Array<Strip>();

        $(document).keypress(this.handleKeyDownEvent);

        this.getStripsFromServer();
    }

    handleKeyDownEvent(e: JQueryKeyEventObject) {
        console.log("key pressed");
    }

    getStripsFromServer() : void {
        var stripApiUrl = this.endPoint + "api/v1/strips/";
        $.ajax({
            url: stripApiUrl,
            method: 'get',
            success: (result, status, xhr) => {
                for(var i = 0; i < result.length; i++) {
                    var stripObj = result[i];
                    var templateName = stripObj.template;

                    if (!this.templates.hasOwnProperty(templateName)) {
                        /* this method is executed synchronously, as the entire
                           callback is async anyway. */
                        this.compileTemplate(templateName);
                    }
                    var template = this.templates[templateName];
                    var strip = new Strip(stripObj, template);

                    this.$target.append(strip.render());
                    this.strips.push(strip);
                }
            }
        });
    }

    advanceToNextStrip() : void {
        if (this.currentStripIdx == this.strips.length - 1) {
            return;
        }

        this.advanceToStrip(this.strips[this.currentStripIdx + 1]);
    }

    advanceToStrip(strip: Strip) : void {
        this.strips[this.currentStripIdx].reset();
    }

    compileTemplate(template: string) {
        var templatesBaseDir = this.endPoint + "static/templates/";
        var templateUrl = templatesBaseDir + template + ".handlebars";
        $.ajax({
            url: templateUrl,
            method: 'get',
            async: false,
            success: (args) => {
                this.templates[template] = Handlebars.compile(args);
            }
        });
    }
}

(function($, endpoint) {
    $(document).ready(function() {
        var manager = new ComicsManager($("#strips-list"), endpoint);
    });
})(jQuery, SERVER_ENDPOINT);
