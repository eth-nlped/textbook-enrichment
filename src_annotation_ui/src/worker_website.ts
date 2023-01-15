import { log_data } from "./connector";
import { DEVMODE } from "./globals";
import { getIndicies } from "./utils";

let main_text_area = $("#main_text_area")
let local_response_template = $("#local_response_template")
let global_response_template = $("#global_response_template")

const zip = (a, b) => a.map((k, i) => [k, b[i]]);

function load_headers() {
    $("#progress").html(`
        <strong>Progress:</strong> ${globalThis.data_i + 1}/${globalThis.data.length}<br>
        <strong>UID:</strong> ${globalThis.uid}
    `)
}

function setup_main_text() {
    // let html_text = `<b>${globalThis.data_now["title"]}</b><br>${globalThis.data_now["text"]}`;
    let out_html = ""
    zip(globalThis.data_now["texts"], globalThis.data_now["imgs"]).forEach((element, s_index) => {
        let text_path = element[0];
        let text_el = `<iframe src="texts/${text_path}" frameborder="0" scrolling="no" onload="resizeIframe(this)"></iframe>`;
        out_html += "<div class='subsection_area'>";
        out_html += text_el;
        let imgs = element[1];
        imgs.forEach((img_path, q_index) => {
            globalThis.responses[`s_${s_index}_q_${q_index}`] = {}
            let response_template = local_response_template.html();
            response_template = response_template.replaceAll("IMAGE_TEMPLATE", img_path);
            // remove lazy loading flag
            response_template = response_template.replaceAll('loading="lazy"', "");
            // remove TEMPLATE flag
            response_template = response_template.replaceAll('template=""', `id="s_${s_index}_q_${q_index}" s_index="${s_index}" q_index=${q_index}`);
            out_html += response_template;
        })
        out_html += "</div>"
    })
    
    out_html += global_response_template.html().replaceAll('template=""', 'id="s_final"')
    main_text_area.html("");
    main_text_area.append($(out_html));

    // select all untemplated ones
    // select radio buttons
    $(".subsection_area:not([template]) div input:not([multiplechoice])").each((index, el) => {
        $(el).on("click", (event) => {
            let parent = $($(el).parents(".active_response_area")[0])
            let parent_id = parent.attr("id")
            let group = $(el).attr("group")

            // clear selection from siblings
            let siblings = $(`#${parent_id} input[group="${group}"]`)
            siblings.each((_, el) => {
                $(el).removeAttr("responseselect")
            })
            $(el).attr("responseselect", "true")
            globalThis.responses[parent_id][group]=$(el).val()
        })
    })

    // select multiple choice buttons
    $(".subsection_area:not([template]) div input[multiplechoice]").each((index, el) => {
        $(el).on("click", (event) => {
            let parent = $($(el).parents(".active_response_area")[0])
            let parent_id = parent.attr("id")
            let group = $(el).attr("group")

            if (globalThis.responses[parent_id][group] == undefined) {
                globalThis.responses[parent_id][group] = {}
            }

            if ($(el).attr("responseselect")) {
                delete globalThis.responses[parent_id][group][$(el).val() as string]
                $(el).removeAttr("responseselect")
            } else {
                globalThis.responses[parent_id][group][$(el).val() as string] = "ok"
                $(el).attr("responseselect", "true")
            }
        })
    })
}

function load_cur_text() {
    globalThis.responses = {}
    globalThis.responsesExpectedCount = 0
    load_headers()
    setup_main_text()
}

function load_thankyou() {
    // TODO: wait for data sync
    load_headers()
    let html_text = `Thank you for participating in our study. `;
    if (globalThis.uid.startsWith("prolific_pilot_1")) {
        html_text += `<br>Please click <a href="https://app.prolific.co/submissions/complete?cc=C67G3X5Y">this link</a> to go back to Prolific. `
        html_text += `Alternatively use this code <em>C67G3X5Y</em>.`
    }
    main_text_area.html(html_text);
}

function setup_navigation() {
    $("#but_next").on("click", () => {
        globalThis.data_i += 1;

        // globalThis.data_log.times.push(Date.now())
        // log_data(globalThis.data_log)

        if (globalThis.data_i >= globalThis.data.length) {
            globalThis.data_i = 0;
            load_thankyou()
        } else {
            globalThis.data_now = globalThis.data[globalThis.data_i];
            load_cur_text()
        }

        $("#but_prev").prop("disabled", globalThis.data_i == 0);
        $("#but_next").prop("disabled", globalThis.data_i == globalThis.data.length-1);
    })

    $("#but_prev").on("click", () => {
        globalThis.data_i -= 1;
        $("#but_prev").prop("disabled", globalThis.data_i == 0);
        $("#but_next").prop("disabled", globalThis.data_i == globalThis.data.length-1);

        globalThis.data_now = globalThis.data[globalThis.data_i];
        load_cur_text()
    })

    $("#but_prev").prop("disabled", true);
}


export { setup_navigation, load_cur_text }