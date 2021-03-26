
//статус завершен

function getStatusSuccess(id){
  $.get('/contract/status-success/'+id, function(data) {
    $('#status3'+id).html("<span class='badge badge-success'>Завершен</span>")
    $('#tr_1'+id).css('background-color', '#0ef34a26');
      console.log('Загрузка завершена.');
    });
}


// статус удален

function delStatusSuccess(id){
  $.get('/contract/status-del/'+id, function(data) {
    $('#status3'+id).html("<span class='badge badge-danger'>Удален</span>")
    $('#tr_1'+id).css('background-color', '#FFD7D7');
      console.log('Удален');
    });
}


// отправка запроса для парсинга с базы stat uz


function getPage(id){
    var inn = $('#clientinn'+id).val();
    var captcha = $('#captcha'+id).val();
    var path = 'contract/get-capcha-statuz';
    $.get(path, function(data) {
          $('#capcha_t').html(data);
          $('#update_btn'+id).hide();
          $('#btn_html'+id).html('<button type="button" class="btn btn-secondary" onclick="getStatuz('+id+')" id="getBtn{{contract.id}}">Получить</button>');
    });
}


function getStatuz(id){
    var inn = $('#clientinn'+id).val();

     $.get('/contract/get-page-statuz/'+inn, function(data) {
        $('#form_contract'+id).html(data);
    });
}

