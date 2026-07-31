<arg_value>const fs = require("fs");
    const f = "c:/Users/varas/personalities/cookbook/website-next/scripts/generate_legal_pages.js";
    let t = fs.readFileSync(f, "utf8");
    const BT = String.fromCharCode(96);
    if (t.startsWith(BT)) {
        t = t.slice(1);
    fs.writeFileSync(f, t, "utf8");
    console.log("stripped stray backtick, new len=" + t.length);
} else {
        console.log("no stray backtick, first char code=" + t.charCodeAt(0));
}