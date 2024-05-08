function copyURL() {
    // Get the text field
    var copyText = document.getElementById("short_url");

    // Select the text field
    copyText.select();
    copyText.setSelectionRange(0, 99999); // For mobile devices

    // Copy the text inside the text field
    navigator.clipboard.writeText(copyText.value);
  }

  function qrcode() {
    if (document.getElementById('qrcode').style.display == 'block') {
      document.getElementById('qrcode').style.display = 'none';
    }
    else {
      document.getElementById('qrcode').style.display = 'block';
    }
}