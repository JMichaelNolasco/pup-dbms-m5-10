$(function (){
var check = [];

function onFormSubmit(event){
	

	var data= $(event.target).serializeArray();
	var thesis = {};
	for (var i=0; i<data.length; i++){
		thesis[data[i].name] = data[i].value		
	}
	//send data to server
	var thesis_create_api = '/api/thesis';	
	$.post(thesis_create_api,thesis,function(response){	 //url,data,callback
		if (response.status = "ok"){
			console.log("Thesis API Response Ok!");
		}});		

	var list_element=$('<li id="item"' +'class="' + thesis.year + thesis.title + '">');
	list_element.html(thesis.year + ' ' + thesis.title + ' '  + ' <input type=button class="buttn btn-danger  btn-xs" value="Delete"  > ');	
	if  ($('ul.thesis-list li').hasClass(thesis.year + thesis.title))
	{
		alert('Duplicate entries found! .Try Again');
	}
	else
	{
		// $(".thesis-list").prepend(list_element) ;
		// check.push(thesis.year + ' ' + thesis.title);
	}
	 return false;
}


function loadAllthesis_list() {
	var thesis_list_api = '/api/thesis';

	$.get(thesis_list_api, {}, function(response){
	console.log('thesis list', response)
	response.data.forEach(function(thesis){
	$('table tr:first').after('<tr></tr>');
    $('tr:eq(1)').append('<td>'+ thesis.year + '</td>');
    $('tr:eq(1)').append('<td>'+ thesis.title + '</td>') ;
    $('tr:eq(1)').append('<td>'+ thesis.author + '</td>');
    $('tr:eq(1)').append('<td>'+  (' <a  href=\'thesis/edit/'+thesis.id+'\'>Edit</a>')+ ' ' + ('<a href=\'thesis/delete/'+thesis.id+'\'>Delete</a>')+ '</td>') ;
	
});
});
};

function UserRegistration(event) {
        var data = $(event.target).serializeArray();

        var user = {};
        for (var i = 0; i < data.length; i++) {
            user[data[i].name] = data[i].value 
        }

        var users_create_api = '/api/user';
        $.post(users_create_api,user,function(response){	 //url,data,callback
		if (response.status = "ok"){
			alert("Succesful Registration")
			console.log("Users API Response Ok!");
			$(location).attr('href', '/home');
		}});

     
    }

$('.registration').submit(UserRegistration)


	
function Users_list() {
	var users_list_api = '/api/user';
	$.get(users_list_api, {}, function(response){
	console.log('user list', response)
	response.data.forEach(function(user){
	$('table tr:first').after('<tr></tr>');
	// $('tr:eq(1)').append('<td >'+ user.email + '</td>');
    $('tr:eq(1)').append('<td >'+ user.first_name + ' ' + user.last_name + '</td>');

    // $('tr:eq(1)').append('<td >'+ user.last_name + '</td>') ;
    // $('tr:eq(1)').append('<td >'+ user.phone_number + '</td>') ;
	
});
});
};

function DeleteEntry(event){
	$(this).parent().remove();
	$(this).closest('li').remove();
				
}
$(document).on('click',  '.buttn' , DeleteEntry)

$('.create-form').submit(onFormSubmit)
	loadAllthesis_list();	

$('.create-form').submit(function(onFormSubmit){ 
    this.reset();
    location.reload(true);
});
//For Phone Number
 $('input#contact').keyup(function(){
        if (
            ($(this).val().length > 0) && ($(this).val().substr(0,3) != '+63')
            || ($(this).val() == '')
            ){
            $(this).val('+63');    
        }
    });



});





// Module 5