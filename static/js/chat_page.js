const send_message = (author) => {
    text_area = document.getElementById("new_message_area")
    msg = text_area.value
    fetch("/new_message/", {
        method: "post",
        headers: { "Content-type": "application/x-www-form-urlencoded; charset=UTF-8" },
        body: `username=${author}&message=${msg}`
    })
    let chat_window = document.getElementById("chat_window");
    chat_window.value += `${author}:\n${msg}\n\n`;
    text_area.value = ""
}

const get_messages = () => {
    fetch("/messages/")
        .then((response) => {
            
            return response.json();
        })
        .then((results) => {
            console.log(results);
            let chat_window = document.getElementById("chat_window");
            let messages = "";
            for (let index in results) {
                current_set = results[index];
                console.log(current_set)
                messages += `${current_set.username}:\n${current_set.message}\n\n`;
            }
            chat_window.value = messages;
        })
        .catch(() => {
            chat_window.value = "error retrieving messages from server";
        });
}

const main = () => {
    get_messages();
    window.setInterval(get_messages, 15000);
}

