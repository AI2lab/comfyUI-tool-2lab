import { ComfyWidgets } from "/scripts/widgets.js";
import { ComfyApp, app } from "/scripts/app.js";
import { api } from '../../../scripts/api.js'
import { applyTextReplacements } from "../../scripts/utils.js";

app.registerExtension({
	name: "Comfy.2lab.nodes",
	async beforeRegisterNodeDef(nodeType, nodeData, app) {

    // Adds an upload button to the nodes
    if (nodeData?.input?.required?.image?.[1]?.image_upload === true) {
        nodeData.input.required.upload = ["IMAGEUPLOAD"];
    }

    if (nodeData.name === "PublishWorkflow (2lab)") {
        const widgets_count = 4;          //PublishWorkflow初始状态是4个参数
        function populate(text) {
//            console.log('populate() nodeData = ',nodeData.name)
//            console.log('text = ',text)
            // 移除在初始状态上增加的widgets
            if (this.widgets) {
//                console.log('widgets_count = ',widgets_count)
//                console.log('this.widgets.length = ',this.widgets.length)
                for (let i = widgets_count; i < this.widgets.length; i++) {
                    this.widgets[i].onRemove?.();
                }
                this.widgets.length = widgets_count;
            }

            const v = [...text];
            var msg = ''
            if(v.length == 1){      //from class PublishWorkflow
                msg = v[0];
                const w = ComfyWidgets["STRING"](this, "text", ["STRING", { multiline: true }], app).widget;
                console.log('w = ',w)
                w.inputEl.readOnly = true;
                w.inputEl.style.opacity = 0.6;
                w.value = msg;

                requestAnimationFrame(() => {
                    const sz = this.computeSize();
                    if (sz[0] < this.size[0]) {
                        sz[0] = this.size[0];
                    }
                    if (sz[1] < this.size[1]) {
                        sz[1] = this.size[1];
                    }
                    this.onResize?.(sz);
                    app.graph.setDirtyCanvas(true, false);
                });
           }
        }

        // When the node is executed we will be sent the input text, display this in the widget
        const onExecuted = nodeType.prototype.onExecuted;
        nodeType.prototype.onExecuted = function (message) {
//                console.log('message = ',message)
            onExecuted?.apply(this, arguments);
            populate.call(this, message.text);
        };

        const onConfigure = nodeType.prototype.onConfigure;
        nodeType.prototype.onConfigure = function () {
            onConfigure?.apply(this, arguments);
            if (this.widgets_values?.length) {
                populate.call(this, this.widgets_values);
            }
        };
    }

    if (nodeData.name === "OutputImage (2lab)") {
			const onNodeCreated = nodeType.prototype.onNodeCreated;
			// When the SaveImage node is created we want to override the serialization of the output name widget to run our S&R
			nodeType.prototype.onNodeCreated = function () {
				const r = onNodeCreated ? onNodeCreated.apply(this, arguments) : undefined;

				const widget = this.widgets.find((w) => w.name === "filename_prefix");
				widget.serializeValue = () => {
					return applyTextReplacements(app, widget.value);
				};

				return r;
			};
		}

    if (nodeData.name === "OutputText (2lab)") {
        function populate(text) {
            if (this.widgets) {
                for (let i = 1; i < this.widgets.length; i++) {
                    this.widgets[i].onRemove?.();
                }
                this.widgets.length = 1;
            }

            const v = [...text];
            if (!v[0]) {
                v.shift();
            }
            for (const list of v) {
                const w = ComfyWidgets["STRING"](this, "text", ["STRING", { multiline: true }], app).widget;
                w.inputEl.readOnly = true;
                w.inputEl.style.opacity = 0.6;
                w.value = list;
            }

            requestAnimationFrame(() => {
                const sz = this.computeSize();
                if (sz[0] < this.size[0]) {
                    sz[0] = this.size[0];
                }
                if (sz[1] < this.size[1]) {
                    sz[1] = this.size[1];
                }
                this.onResize?.(sz);
                app.graph.setDirtyCanvas(true, false);
            });
        }

        // When the node is executed we will be sent the input text, display this in the widget
        const onExecuted = nodeType.prototype.onExecuted;
        nodeType.prototype.onExecuted = function (message) {
            onExecuted?.apply(this, arguments);
            populate.call(this, message.text);
        };

        const onConfigure = nodeType.prototype.onConfigure;
        nodeType.prototype.onConfigure = function () {
            onConfigure?.apply(this, arguments);
            if (this.widgets_values?.length) {
                populate.call(this, this.widgets_values);
            }
        };
    }
	},
});

//api.addEventListener('execution_start', async ({ detail }) => {
//  console.log('#execution_start 2lab', detail)
//    try{
//
//              }
//            }
//        }
//      }
//    } catch (error) {
//        console.log('###error', error)
//    }
//})

