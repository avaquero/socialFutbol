function Comentar(id) {
	document.getElementById('publicacio').value = id;
}


$(document).ready(function() {
	$('#id_busca').keyup(function() {
		$('#buscar').empty();
		var nom = document.getElementById('id_busca').value;
		var domini = "http://127.0.0.1:8000";
		$.ajax({
			url : domini + "/perfil/buscar",
			type : "GET",
			dataType : "json",
			data : {
				cadena : nom,
			}, //fi data
			success : function(perfils) {
				$("#buscar").append("<ul class='list-group' id='llista'></ul>");
				$.each(perfils, function() {
					var id = this['pk'];
					var nom = this['fields']['nom'];
					var cognoms = this['fields']['cognoms'];
					var imatge = this['fields']['imatgePerfil'];

					if (imatge) {
						$('#llista').append("<a href='" + domini + "/perfil/" + id + "' class='list-group-item'>" + "<img src='/media/" + imatge + "' width='50px' height='50px' class='img-responsive' alt='Imatge perfil' />" + nom + " " + cognoms + "</a>");
					} else {
						$('#llista').append("<a href='" + domini + "/perfil/" + id + "' class='list-group-item'>" + "<img src='/static/imatges/default.jpg' width='50px' height='50px' class='img-responsive' alt='Imatge perfil' />" + nom + " " + cognoms + "</a>");
					}

				});
				//fi function
			}, //fi succes
			error : function(xhr, errmsg, err) {
				$('#buscar').append('<p>Error</p>');
			}
		});
		//fi ajax
		return false;
	});
	//fi idbusca

});
// fi ready
