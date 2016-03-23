$(document).ready(function() {
            // Configure/customize these variables.
            var showChar = 340;  // How many characters are shown by default
            var ellipsestext = "...";
            var moretext = "read more";
            var lesstext = "read less";


            $('.more').each(function() {
                var content = $(this).html();

                if(content.length > showChar) {

                    var c = content.substr(0, showChar);
                    var h = content.substr(showChar, content.length - showChar);

                    var html = c +  '<span class="morecontent"><span>' + h + '</span>&nbsp;&nbsp;<p><a href="" class="morelink theme-btn btn-theme-one">' + moretext + '</a><p></span>';

                    $(this).html(html);
                }

            });

            $(".morelink").click(function(){
                if($(this).hasClass("less")) {
                    $(this).removeClass("less");
                    $(this).html(moretext);
                } else {
                    $(this).addClass("less");
                    $(this).html(lesstext);
                }
                $(this).parent().prev().toggle();
                $(this).prev().toggle();
                return false;
            });
        });
