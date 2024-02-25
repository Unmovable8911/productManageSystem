var dates = document.getElementsByClassName("date");

var manufactureDateInput = document.getElementById('id_manufacture_date');
var shelfLifeInput = document.getElementById('id_shelf_life');
var shelfLifeUnitInput = document.getElementById('id_shelf_life_unit');
var expireDateInput = document.getElementById('id_expire_date');

var catagoryDialog = document.getElementById("catagory-dialog");
var blur = document.getElementById("blur");

for (let date of dates) {
    let dateObject = new Date(date.textContent);
    date.textContent = dateObject.toISOString().slice(0,10);
}

function calculateExpirationDate() {
    // Check if manufacture date shelf life and shelf life unit are filled
    let manuDateFilled = (manufactureDateInput.value != "");
    let shelfLifeFilled = (shelfLifeInput.value != "");
    let shelfLifeUnitFilled = (shelfLifeUnitInput.value != "");

    if (manuDateFilled && shelfLifeFilled && shelfLifeUnitFilled) {
        // Parse the manufacture date input value
        let manufactureDate = new Date(manufactureDateInput.value);

        // Get the shelf life and shelf life unit values
        let shelfLife = parseFloat(shelfLifeInput.value);
        let shelfLifeUnit = shelfLifeUnitInput.value;

        // Calculate the expiration date based on the shelf life unit
        let expirationDate = new Date(manufactureDate);
        if (shelfLifeUnit === '天') {
        expirationDate.setDate(manufactureDate.getDate() + shelfLife);
        } else if (shelfLifeUnit === '月') {
        expirationDate.setMonth(manufactureDate.getMonth() + shelfLife);
        }

        // Set the expiration date input value
        expireDateInput.value = expirationDate.toISOString().slice(0, 10);
    }
}

// Attach the calculateExpirationDate function to the input events of manufacture date and shelf life
manufactureDateInput.addEventListener('change', calculateExpirationDate);
shelfLifeInput.addEventListener('input', calculateExpirationDate);
shelfLifeUnitInput.addEventListener('change', calculateExpirationDate);

// Call the calculateExpirationDate function initially to set the initial expiration date
calculateExpirationDate();

// New catagory dialog
function openCatagoryDialog() {
    catagoryDialog.style.display = "block";
    blur.style.display = "block";
}

function closeCatagoryDialog() {
    catagoryDialog.style.display = "none";
    blur.style.display = "none";
}
