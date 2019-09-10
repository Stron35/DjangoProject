$(document).ready(function(){
        $("#carousel").carousel({
        	interval: 2000
        });
});

function fileInputChange(input) {
    var text = (input.files.length > 0) ? 'Choosing files: ' + input.files.length : 'Choose file';
    input.parentNode.getElementsByTagName('label')[0].innerText = text;
  }