
function checkCheckbox() {
    const check1 = document.getElementById("vac");
    const check2 = document.getElementById("req");
    if (!check1.checked){
        check1.value = "";
    } else{
        check1.value = "true";
    };
    if (!check2.checked){
        check2.value = "";
    } else{
        check2.value = "true";
    };
};

function callBack(data) {
    console.log(data);
}

async function callAPI(url) {
    let response = {};
    let query = [];
    if (url){
        let resp = await fetch(url);
        response = await resp.json();
        query = url
        console.log(response)
        
    } else {
        console.log("No query")
        query = "";
    };
    response = JSON.stringify(response, null, 4);
    return [query, response];
}