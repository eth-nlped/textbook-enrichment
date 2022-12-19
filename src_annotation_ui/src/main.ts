import { DEVMODE } from "./globals"
export var UID: string
import { load_data } from './connector'
import { setup_navigation, load_cur_text } from "./worker_website"
import { range } from "./utils";

globalThis.phase = -1;
globalThis.data = null

const urlParams = new URLSearchParams(window.location.search);
globalThis.uid = urlParams.get('uid');
// take data_i from GET if available else use 0 as default
globalThis.data_i = parseInt(urlParams.get("data_i"))-1 || 0;

function prolific_rewrite_uid(uid) {
    if (uid != "prolific_onestopqa_pilot_1") {
        return uid
    }

    let slots = range(0, 99).map((x) => String(x).padStart(2, "0"));
    let slot = slots[Math.floor(Math.random() * slots.length)];

    globalThis.prolific_pid = urlParams.get('prolific_pid');
    console.log(globalThis.prolific_pid)

    return `prolific_onestopqa_pilot_1/s${slot}`
}

async function get_uid_and_data() {
    // repeat until we're able to load the data
    while (globalThis.data == null) {
        if (globalThis.uid == null) {
            let UID_maybe = null
            while (UID_maybe == null) {
                UID_maybe = prompt("What is your user id?")
            }
            globalThis.uid = UID_maybe!;
        }

        globalThis.uid = prolific_rewrite_uid(globalThis.uid);

        await load_data().then((data: any) => {
            globalThis.data = data
            globalThis.data_now = globalThis.data[globalThis.data_i];
            setup_navigation()
            load_cur_text()
        }).catch((reason: any) => {
            console.error(reason)
            alert("Invalid UID " + globalThis.uid);
            globalThis.uid = null;
        });
    }
}

get_uid_and_data()
