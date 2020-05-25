
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
}

async function callAPI() {
    checkCheckbox();
    let form = document.getElementById("form");
    let query = [];
    let response = {};
    let semester = "";
    for (let i = 0; i < form.length; i++) {
        const element = form.elements[i];
        if (element.type != "submit" && element.name != "semestre") {
            if (!(element.value == "" || element.value == "TODOS")){
                query.push(element.name + "=" + element.value)
            };
        } else if (element.name == "semestre"){
            semester = "semestre=" + element.value;
        };
    };
    if (query.length > 0){
        query.unshift(semester);
        query = 'https://buscacursos-api.herokuapp.com/api/v3?' + query.join("&");
        console.log(query)
        let resp = await fetch(query);
        response = await resp.json();
        console.log(response)
    } else {
        console.log("No query")
        query = "https://buscacursos-api.herokuapp.com/api/v3?";
    };
    response = JSON.stringify(response, null, 4);
    return [query, response];
}