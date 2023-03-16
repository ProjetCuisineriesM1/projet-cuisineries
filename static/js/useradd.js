function strRandom(o) {
    var a = 10,
        b = 'abcdefghijklmnopqrstuvwxyz',
        c = '',
        d = 0,
        e = ''+b;
    if (o) {
        if (o.startsWithLowerCase) {
        c = b[Math.floor(Math.random() * b.length)];
        d = 1;
        }
        if (o.length) {
        a = o.length;
        }
        if (o.includeUpperCase) {
        e += b.toUpperCase();
        }
        if (o.includeNumbers) {
        e += '1234567890';
        }
    }
    for (; d < a; d++) {
        c += e[Math.floor(Math.random() * e.length)];
    }
    return c;
    }
function updateRole(role){
    console.log(role)
    if(role === "Adhérent"){
        document.getElementsByName("referent")[0].removeAttribute("disabled");
        document.getElementsByName("referent")[0].setAttribute("required", "required");
    }else{
        document.getElementsByName("referent")[0].removeAttribute("required");
        document.getElementsByName("referent")[0].setAttribute("disabled", "disabled");
    }
}
function validateForm1(){
    if(document.getElementById("firstname").value == ""){
        document.getElementById("firstname").classList.add("is-invalid");
        document.getElementById("firstnameError").style.display = 'block';
        return;
    }else{
        document.getElementById("firstnameError").style.display = 'none';
        document.getElementById("firstname").classList.remove("is-invalid");
    }
    if(document.getElementById("lastname").value == ""){
        document.getElementById("lastname").classList.add("is-invalid");
        document.getElementById("lastnameError").style.display = 'block';
        return;
    }else{
        document.getElementById("lastnameError").style.display = 'none';
        document.getElementById("lastname").classList.remove("is-invalid");
    }
    if(document.getElementById("role").value == "0"){
        document.getElementById("role").classList.add("is-invalid");
        document.getElementById("roleError").style.display = 'block';
        return;
    }else{
        document.getElementById("roleError").style.display = 'none';
        document.getElementById("role").classList.remove("is-invalid");
    }
    if(document.getElementById("referent").value == "0" && document.getElementById("role").value == "Membre"){
        document.getElementById("referent").classList.add("is-invalid");
        document.getElementById("referentError").style.display = 'block';
        return;
    }else{
        document.getElementById("referentError").style.display = 'none';
        document.getElementById("referent").classList.remove("is-invalid");
    }
    if(document.getElementById("username").value == ""){
        document.getElementById("username").classList.add("is-invalid");
        document.getElementById("usernameError").style.display = 'block';
        return;
    }else{
        document.getElementById("usernameError").style.display = 'none';
        document.getElementById("username").classList.remove("is-invalid");
    }
    if(document.getElementById("telephone").value == ""){
        document.getElementById("telephone").classList.add("is-invalid");
        document.getElementById("telephoneError").style.display = 'block';
        return;
    }else{
        document.getElementById("telephoneError").style.display = 'none';
        document.getElementById("telephone").classList.remove("is-invalid");
    }
    if(document.getElementById("email").value == ""){
        document.getElementById("email").classList.add("is-invalid");
        document.getElementById("emailError").style.display = 'block';
        return;
    }else{
        document.getElementById("emailError").style.display = 'none';
        document.getElementById("email").classList.remove("is-invalid");
    }
    document.getElementById("form_part1").style.display = "none";
    document.getElementById("form_part2").style.display = "flex";

    let password = strRandom({
        includeUpperCase: true,
        includeNumbers: true,
        length: 8,
        startsWithLowerCase: true
    });

    let form = new FormData();

    form.append("firstname", document.getElementById("firstname").value);
    form.append("lastname", document.getElementById("lastname").value);
    form.append("role", document.getElementById("role").value);
    form.append("referent", document.getElementById("referent").value);
    form.append("username", document.getElementById("username").value);
    form.append("email", document.getElementById("email").value);
    form.append("telephone", document.getElementById("telephone").value);
    form.append("password", password);
    form.append("step", 1)
    let csrfTokenValue = document.querySelector('[name=csrfmiddlewaretoken]').value;
    let request = new Request("/ajax/newuser", {method: 'POST',
                                                step: 1,
                                                body: form,
                                                headers: {"X-CSRFToken": csrfTokenValue}})
    fetch(request)
        .then(response => response.json())
        .then(result => {
            if(result.result){
                document.getElementById('resultStep1').innerHTML = "<span>Mot de passe : "+password+"</span>";
                document.getElementById('buttonPart2').innerText = "Ajouter une photo";
                document.getElementById('id_newUser').value = result.id;
                document.getElementById('buttonPart2').removeAttribute("disabled");
            }else{
                alert("Une erreur est survenue !");
            }
        });

    return false;

}
function validateForm2(){
    document.getElementById("form_part2").style.display = "none";
    document.getElementById("form_part3").style.display = "flex";
}

function traiterImageUpload(){
    document.getElementById('photo').src = URL.createObjectURL(document.getElementById("profil_picture").files[0]);
    document.getElementById('resultStep3').style.display = "block";
    let form = new FormData();

    form.append("picture", document.getElementById("profil_picture").files[0]);
    form.append("step", 2);
    form.append("id_user", document.getElementById('id_newUser').value);

    let csrfTokenValue = document.querySelector('[name=csrfmiddlewaretoken]').value;
    let request = new Request("/ajax/newuser", {method: 'POST',
                                                body: form,
                                                headers: {"X-CSRFToken": csrfTokenValue}})
    fetch(request)
        .then(response => response.json())
        .then(result => {
            if(result.result){
                document.getElementById('photo').setAttribute('src', result.src);
                document.getElementById('resultStep3').style.display = "none";
                document.getElementById('photo').style.opacity = "1";
                document.getElementById('photo').style.display = "inline";
                document.getElementById('valid_photo').style.display = "inline-block";
            }else{
                alert("Une erreur est survenue !");
            }
        });
}

function validatePicture(){

    let form = new FormData();

    form.append("step", 4);
    form.append("id_user", document.getElementById('id_newUser').value);

    let csrfTokenValue = document.querySelector('[name=csrfmiddlewaretoken]').value;
    let request = new Request("/ajax/newuser", {method: 'POST',
                                                body: form,
                                                headers: {"X-CSRFToken": csrfTokenValue}})
    fetch(request)
        .then(response => response.json())
        .then(result => {
            if(result.result){
                document.getElementById("form_part3").style.display = "none";
                window.location.href = "/profil/"+document.getElementById('id_newUser').value;
            }else{
                alert("Une erreur est survenue !");
            }
        });
}