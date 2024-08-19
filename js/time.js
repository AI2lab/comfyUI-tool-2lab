import { ComfyApp, app } from "/scripts/app.js";
import { api } from '../../../scripts/api.js'

app.registerExtension({
	name: "Comfy.2lab.time",
    async setup() {
        api.addEventListener('execution_start', async ({ detail }) => {
          console.log('#execution_start')
//          console.log('prompt_id = ', detail.prompt_id)
//          console.log('timestamp = ', detail.timestamp)
        })
        api.addEventListener('execution_success', async ({ detail }) => {
          console.log('#execution_success')
//          console.log('prompt_id = ', detail.prompt_id)
//          console.log('timestamp = ', detail.timestamp)
        })
    }
})