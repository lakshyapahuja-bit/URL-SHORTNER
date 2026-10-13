const BASE_URL = "http://127.0.0.1:8000";

const shortenbtn = document.querySelector("#shortenBtn");
const originalurl = document.querySelector("#originalUrl");
const shortresult = document.querySelector("#shortResult");

shortenbtn.addEventListener("click", async (evt) => {
    evt.preventDefault();

    let url = originalurl.value;

    if(url === "")
    {
        alert("Please enter a URL");
        return;
    }

    let response = await fetch(`${BASE_URL}/shorten`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            original: url
        })
    });

    let data = await response.json();

    if(!response.ok)
    {
        shortresult.innerText = data.detail;
        return;
    }

    shortresult.innerText = data.short_url;
});


const redirectbtn = document.querySelector("#redirectBtn");
const shorturl = document.querySelector("#shortUrl");

redirectbtn.addEventListener("click", (evt) => {
    evt.preventDefault();

    let url = shorturl.value;

    if(url === "")
    {
        alert("Please enter a short URL");
        return;
    }

    window.location.href = url;
});


const statsbtn = document.querySelector("#statsBtn");
const statsurl = document.querySelector("#statsUrl");
const statsresult = document.querySelector("#statsResult");

statsbtn.addEventListener("click", async (evt) => {
    evt.preventDefault();

    let code = statsurl.value;

    if(code === "")
    {
        alert("Please enter a short URL");
        return;
    }

    if(code.includes("/"))
    {
        code = code.split("/").pop();
    }

    let response = await fetch(`http://127.0.0.1:8000/stats/${code}`);

    let data = await response.json();

    if(!response.ok)
    {
        statsresult.innerText = data.detail;
        return;
    }

    statsresult.innerText = `Click Count: ${data.click_count}`;
});