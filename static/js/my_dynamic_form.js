$(document).ready(function(){

    $("#add").click(function (e){
        event.preventDefault()
        $('#items').append('<div class="h5 mb-0 font-weight-bold text-gray-800">Address</div>'+
        '<div class="row"> <!-- Start of embedded row (within the card) -->'+
                    '<!-- Data Source 1 Select Address Card Example -->'+
                    '<div class="col-xl-6 col-md-6 mb-4">'+
                      '<div class="card border-left-primary shadow h-100 py-2">'+
                        '<div class="card-body">'+
                          '<div class="row no-gutters align-items-center">'+
                            '<div class="col mr-2">'+
                              '<div class="text-xs font-weight-bold text-primary text-uppercase mb-1">Data Source 1 - Address</div>'+
                              '<div class="container">'+
                                '<select name= datasource1_schema method="POST" action="/">'+
                                  '{% for item in datasource1_schema %}'+
                                  '<option value= "{{item}}">{{item}}</option>"'+
                                  '{% endfor %}'+
                                '</select>'+     
                            '</div> <!-- end of div before form-->'+
                            '</div>'+
                            '<div class="col-auto">'+
                              '<i class="fas fa-file-alt fa-2x text-gray-300"></i>'+
                            '</div>'+
                          '</div>'+
                        '</div>'+
                      '</div>'+
                    '</div>'+
                    '<!-- Data Source 2 Select Address Card Example -->'+
                    '<div class="col-xl-6 col-md-6 mb-4">'+
                      '<div class="card border-left-success shadow h-100 py-2">'+
                        '<div class="card-body">'+
                          '<div class="row no-gutters align-items-center">'+
                            '<div class="col mr-2">'+
                              '<div class="text-xs font-weight-bold text-success text-uppercase mb-1">Data Source 2 - Address</div>'+
                              '<div class="container">'+
                                '<form action="/some_php_page.php">'+
                                  '<fieldset>'+
                                    '<select name= datasource2_schema method="POST" action="/">'+
                                      '{% for item in datasource2_schema %}'+
                                      '<option value= "{{item}}">{{item}}</option>"'+
                                      '{% endfor %}'+
                                    '</select>'+     
                            '</div> <!-- end of div before form-->'+
                            '</div>'+
                            '<div class="col-auto">'+
                              '<i class="fas fa-file-alt fa-2x text-gray-300"></i>'+
                            '</div>'+
                          '</div>'+
                        '</div>'+
                      '</div>'+
                    '</div>'+
        '</div> <!-- end of embedded row -->');
    });

    $('body').on('click','#delete',function (e){
        $(this).parent('div').remove();
    });
});