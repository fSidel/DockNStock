$(document).ready(function() {

    $('.like.pulsante').click(function() {
        
        var pkey = $(this).val(); 
        
        var but = document.getElementById('likebtn' + pkey);
        $.ajax({
            url: "/leavealike",
            type: 'POST',
            data: {
                'primarykey': pkey,
            }, 

            dataType: 'json',
            success: function(data) {
                var code = data.code;
                if(code === '200'){
                    
                    but.style.backgroundColor = "red";
                    but.style.fontSize = "clamp(1.2rem ,2.8vw, 3.5rem)";


                }
                else if (code === '201') {
                    but.style.backgroundColor = "#efff14";
                    but.style.fontSize = "clamp(1rem, 1.3vw, 2rem)";


                }
                else{
                    console.log("Something failed..."); 
                }

            },

            error: function(text, error) { 

                console.error('Error: ' + text, error);
            }
        });
    });

    $('.like.pulsante2').click(function() {
        var pkey = $(this).val(); 
        var sav = document.getElementById('savebtn' + pkey);
        
        $.ajax({
            url: "/addtowants",
            type: 'POST',
            data: {
                'primarykey': pkey,
            }, 

            dataType: 'json',
            success: function(data) {
                var code = data.code;
                if(code === '200'){
                    sav.style.backgroundColor = "black";
                    sav.style.color = "white";
                    sav.style.fontSize = "clamp(1.2rem ,2.8vw, 3.5rem)";

                }
                else if (code === '201') {
                    sav.style.backgroundColor = "#efff14";
                    sav.style.color = "black";
                    sav.style.fontSize = "clamp(1rem, 1.3vw, 2rem)";

                }
                else{
                    console.log("Something failed...");
                }  
            },

            error: function(text, error) { 

                console.error('Error: ' + text, error);
            }
        });
    });

    $(".foto").dblclick(function(){
        var pkey = $(this).data('value'); 

        var heart = document.getElementById('cuore' + pkey);
        var but = document.getElementById('likebtn' + pkey);
        
        $.ajax({
            url: "/leavealike",
            type: 'POST',
            data: {
                'primarykey': pkey,
            }, 

            dataType: 'json',
            success: function(data) {
                var code = data.code;
                if(code === '200'){
                    but.style.backgroundColor = "red";
                    but.style.fontSize = "clamp(1.2rem ,2.8vw, 3.5rem)";

                }
                else if (code === '201') {
                    but.style.backgroundColor = "#efff14";
                    but.style.fontSize = "clamp(1rem, 1.3vw, 2rem)";

                }
                else{
                    console.log("Something failed...");
                }  

            },

            error: function(text, error) { 

                console.error('Error: ' + text, error);
            }
        });
    });

    $(".like.pulsante3").click(function(){
        var pkey = $(this).val();
        var modalname = '#exampleModalCenter' + pkey;
        $(modalname).modal('show');
        toggleSubmitButtonColor(pkey); 
    })


    $('.commentForm').submit(function(event) {
        event.preventDefault();
        var pkey = $(this).data('value');
        var text = $("#mycomment"+pkey).val();
        if (text.trim() !== "") {
            
            $.ajax({
                url: "/postcomments",
                type: "POST",
                data: {
                    "comments": text,
                    "product_key": pkey
                },

                dataType: 'json',
                success: function(data) {
                    console.log(data);
                    var mia_email = data;
                    var div = '<div class="comment"><div class="author"><p>'+mia_email+'</p></div><div class="text"><p>' + text + '</p></div></div>';
                    var lcomments = '#listacommenti'+pkey;
                    var mycomment = "#mycomment"+pkey;
                    toggleSubmitButtonColor(pkey);
                    $(lcomments).prepend(div);
                    $(mycomment).val("");
                    toggleSubmitButtonColor(pkey);
                },

                error: function(text, error) { 

                    console.error('Error: ' + text, error);
                }

            });                
        } 
        
    });



    $('.commentForm input').on('input', function() {
        var pkey = $(this).closest('form').data('value');
        toggleSubmitButtonColor(pkey);
    });

});

function toggleSubmitButtonColor(pkey) {
    var commentInput = $("#mycomment" + pkey);
    var submitButton = commentInput.closest('form').find('.pulsante5');
    if (commentInput.val().trim() === "") {
        submitButton.css("background-color", "red");
        submitButton.css("pointer-events", "none");
    } else {
        submitButton.css("background-color", "#efff14f1");
        submitButton.css("pointer-events", "all");
    }
}

function onTop() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

window.onscroll = function() {
    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
        document.getElementById("top").style.display = "block";
    } else {
        document.getElementById("top").style.display = "none";
    }
};

