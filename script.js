document.getElementById("rateToggle").addEventListener("change", function () {
    document.getElementById("rateBlock").style.display =
        this.value === "yes" ? "block" : "none";
});

async function generateEmail() {

    const name = document.getElementById("name").value || "Коллеги";
    const templateFile = document.getElementById("direction").value;
    const rateToggle = document.getElementById("rateToggle").value;

    let response = await fetch("templates/" + templateFile);
    let text = await response.text();

    const load = document.getElementById("loadCity").value;
    const unload = document.getElementById("unloadCity").value;
    const transit = load && unload ? load + " - " + unload : "";

    text = text.replace("{transit}", transit);

    if (rateToggle === "yes") {
        const conditions = document.getElementById("conditions").value;
        const rate = document.getElementById("rate").value;

        let priceBlock = `${conditions} ${transit} - ${rate}`;
        text = text.replace("{price}", priceBlock);

        if (transit && text.includes("{sale}")) {
            text = text.replace("{sale}",
                `Хочу предложить для Вас наши условия и тарифы по маршруту ${transit}.`
            );
        }
    } else {
        text = text.replace("{price}", "");
        text = text.replace("{sale}", "");
    }

    document.getElementById("output").value =
        `${name}, Добрый день!\n\n` + text;
}

function copyText() {
    const output = document.getElementById("output");
    output.select();
    document.execCommand("copy");
}