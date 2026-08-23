function dValidate(){
    var names = document.getElementById('fname') ? document.getElementById('fname').value : '';
    var age = document.getElementById('fage') ? document.getElementById('fage').value : '';
    var weight = document.getElementById('fweight') ? document.getElementById('fweight').value : '';
    var email = document.getElementById('femail') ? document.getElementById('femail').value : '';
    var phone = document.getElementById('fphone') ? document.getElementById('fphone').value : '';
    
    var selectedType = document.querySelector('input[name="ftype"]:checked');
    var type = selectedType ? selectedType.value : (document.getElementById('ftype') ? document.getElementById('ftype').value : '');

    if(names.length < 3){
        alert("Please enter your full name.");
        return false;
    } else if (age.length < 1 || parseInt(age) < 18) {
        alert("Please enter a valid age (18 or older).");
        return false;
    } else if (weight.length < 2 || parseInt(weight) < 45) {
        alert("Please enter a valid weight (minimum 45 kg).");
        return false;
    } else if (email.length < 3 || !email.includes('@')) {
        alert("Please enter a valid email address.");
        return false;
    } else if (phone.length < 7) {
        alert("Please enter a valid phone number.");
        return false;
    } else if (!type || type.length < 1) {
        alert("Please select your blood type.");
        return false;
    }
    return true;
}