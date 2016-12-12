/**
 * Created by Diver on 12.12.2016.
 */

function onChange()
    {
        var f = document.getElementById("id_ie");
        if (!f.checked)
        {
            tax = document.getElementById("id_taxpayer_account_number");
            lic = document.getElementById("id_license_field");
            tax.hidden = true;
            tax.required = "";
            lic.hidden = true;
            lic.required = "";

            document.getElementById("hid1").hidden = true;
            document.getElementById("hid2").hidden = true;
        }
        else
        {
            tax = document.getElementById("id_taxpayer_account_number");
            lic = document.getElementById("id_license_field");
            tax.hidden = false;
            tax.required = "required";
            lic.hidden = false;
            lic.required = "required";

            document.getElementById("hid1").hidden = false;
            document.getElementById("hid2").hidden = false;
        }
    }