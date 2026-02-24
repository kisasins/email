const rateToggle = document.getElementById("rateToggle");
const rateBlock = document.getElementById("rateBlock");

rateBlock.style.display = "none";

rateToggle.addEventListener("change", function () {
    rateBlock.style.display = this.value === "yes" ? "block" : "none";
});

const companyMap = {
    food: "Могунция, Новапродукт",
    candy: "Алютех, Купишуз, Белдор",
    alcohol: "Аливария, Минск Кристалл",
    feed: "Белкорм, Агропродукт"
};

async function generateEmail() {

    const name = document.getElementById("name").value || "Коллеги";
    const templateFile = document.getElementById("direction").value;
    const companyType = document.getElementById("companyType").value;
    const rateEnabled = document.getElementById("rateToggle").value === "yes";

    let response = await fetch("templates/" + templateFile);
    let text = await response.text();

    // COMPANY
    if (text.includes("{company}")) {
        text = text.replace("{company}", companyMap[companyType] || "");
    }

    // TRANSIT
    const load = document.getElementById("loadCity").value;
    const unload = document.getElementById("unloadCity").value;
    const transit = load && unload ? `${load} - ${unload}` : "";

    text = text.replace("{transit}", transit);

    // SALE
    if (text.includes("{sale}")) {
        if (transit) {
            text = text.replace("{sale}",
                `Хочу предложить для Вас наши условия и тарифы по маршруту ${transit}.`
            );
        } else {
            text = text.replace("{sale}", "");
        }
    }

    // PRICE BLOCK
if (rateEnabled) {

    const sea = parseFloat(document.getElementById("sea").value) || 0;
    const rail = parseFloat(document.getElementById("rail").value) || 0;
    const auto = parseFloat(document.getElementById("auto").value) || 0;

    const transportType = document.getElementById("transportType").value;
    const conditions = document.getElementById("conditions").value;

    let priceText = "";

    // ЕСЛИ ТЕНТ ИЛИ РЕФ → обычная котировка
    if (transportType === "тент" || transportType === "реф") {

        const total = sea || rail || auto; // используем одно значение

        priceText = `
${conditions} ${transit}, ${transportType} — ${total} USD
Транзитный срок: 7-14 дней.
`;

    } else {

        // Китай / контейнеры → считаем ALL IN
        const allIn = sea + rail + auto;

        priceText = `
${conditions} ${transit}, ${transportType} — ${allIn} USD

Морской фрахт: ${sea} USD
ЖД фрахт: ${rail} USD
Автовывоз: ${auto} USD
Транзитный срок: 7-14 дней.
`;
    }

    text = text.replace("{price}", priceText);

} else {
    text = text.replace("{price}", "");
}

    // MARKING
    if (document.getElementById("markingCheck").checked) {

        let markResponse = await fetch("templates/marking_template.txt");
        let markText = await markResponse.text();
        text = text.replace("{marking}", markText);

    } else {
        text = text.replace("{marking}", "");
    }

    document.getElementById("output").value =
        `${name}, Добрый день!\n\n` + text;
}

function copyText() {
    const output = document.getElementById("output");
    output.select();
    document.execCommand("copy");
}

