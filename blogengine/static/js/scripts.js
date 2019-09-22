$(document).ready(function(){
        
        ajaxPagination();
        $(".carousel").carousel({
                interval: 1500
            });
        
        $("#id_text").bind("input", function(){
            //Нужно для того, чтобы при отсутствии загружаемого файла, textarea был обязательным
            $("#id_text").prop("required",true);
        }).trigger("input");
        $("#file").bind("input", function(){
            //Если имеется файл или что-то есть в textarea
            if($("#file").val() && (!$.trim($("#id_text").val())||$.trim($("#id_text").val()))){
                $("#id_text").prop("required",false);
                $("#file").prop("required",true);
            }
            else{
                $("#id_text").prop("required",true);
                $("#file").prop("required",false);
            }
        }).trigger("input");
});

// Из-за этого двойное срабатываение
$(document).ajaxStop(function(){
    $('.carousel').carousel();

});

function fileInputChange(input) {
    var text = (input.files.length > 0) ? 'Choosing files: ' + input.files.length : 'Choose file';
    input.parentNode.getElementsByTagName('label')[0].innerText = text;
  }


// Infinite scroll

function ajaxPagination() {
    
    $('a.page-load').each((index, el) => {
        $(el).click((e) =>{
            e.preventDefault()
            let pageUrl = $(el).attr('href') //Берем существующую ссылку
            //Заменяем номер страницы на следующий
            //?page=2-5 2-номер следующей страницы 5-максимальное число страниц
            //pageNumber для создания номера следующей страницы
            //pageUrl == ?page=2
            //newUrl == ?page=3
            //При достижении pageNumber>maxPages удаляет ссылку
            //не работает управление каруселью
            var maxPages = Number(pageUrl.split('-')[1])
            pageNumber = Number((pageUrl.split('-')[0]).split('=')[1])
            pageUrl = pageUrl.split('-')[0]
            newUrl = [[pageUrl.split('=')[0],pageNumber+Number(1)].join('='),maxPages].join('-')

            if (maxPages > pageNumber) {
                $.ajax({
                    url: pageUrl,
                    type: 'GET',
                    success: (data) => {
                        // $('#blog-posts').empty()
                        // $('#blog-posts').append($(data).find('#blog-posts').html(data))
                        $('#blog-posts').append($(data).filter('#blog-posts').html());
                        // $("#blog-posts").load("trackingCode.html script");
                        $(el).attr('href', newUrl);
                        $(".carousel").carousel({});
                        $(".carousel").carousel({
                            interval: 1500
                        });
                    }
                })

            }
            else if (maxPages == pageNumber){
                $.ajax({
                    url: pageUrl,
                    type: 'GET',
                    success: (data) => {
                        $('#blog-posts').append($(data).filter('#blog-posts').html());
                        $(el).prop('hidden', true);
                        $(".carousel").carousel({});
                        $(".carousel").carousel({
                            interval: 1500
                        });
                    }
                })                
            }
        })
    })
}