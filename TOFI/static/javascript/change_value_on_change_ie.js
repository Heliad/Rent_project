/**
 * Created by Diver on 12.12.2016.
 */
function onChange()
    {
        var f = document.getElementById("id_ie");
        var tax = document.getElementById("id_taxpayer_account_number");
        var lic = document.getElementById("id_license_field");
        var hid1 =  document.getElementById("hid1");
        var hid2 =  document.getElementById("hid2");
        if (!f.checked)
        {
            tax.hidden = true;
            tax.required = "";
            lic.hidden = true;
            lic.required = "";

            hid1.hidden = true;
            hid2.hidden = true;
        }
        else
        {
            tax.hidden = false;
            tax.required = "required";
            lic.hidden = false;
            lic.required = "required";

            hid1.hidden = false;
            hid2.hidden = false;
        }
    }