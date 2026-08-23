function rValidate(){
    var names = document.getElementById('fname') ? document.getElementById('fname').value : '';
    var email = document.getElementById('femail') ? document.getElementById('femail').value : '';
    var phone = document.getElementById('fphone') ? document.getElementById('fphone').value : '';
    var details = document.getElementById('fdetails') ? document.getElementById('fdetails').value : '';

    var selectedType = document.querySelector('input[name="ftype"]:checked');
    var type = selectedType ? selectedType.value : (document.getElementById('ftype') ? document.getElementById('ftype').value : '');

    if(names.length < 3){
        alert("Please enter your full name.");
        return false;
    } else if (email.length < 3 || !email.includes('@')) {
        alert("Please enter a valid email address.");
        return false;
    } else if (phone.length < 7) {
        alert("Please enter a valid phone number.");
        return false;
    } else if (!type || type.length < 1) {
        alert("Please select the required blood type.");
        return false;
    } else if (details.length < 5) {
        alert("Please enter your address and details.");
        return false;
    }
    return true;
}