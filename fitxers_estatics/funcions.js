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

					$('#llista').append("<a href='" + domini + "/perfil/" + id + "' class='list-group-item'>" + nom + " " + cognoms + "</a>");

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

	$(window).scroll(function() {
		if ($(window).scrollTop() == $(document).height() - $(window).height()) {
			
			var perfil = document.getElementById('idPerf').value;
			var idMax = document.getElementById('idMax').value;
			var domini = "http://127.0.0.1:8000";
			$.ajax({
				url : domini + "/perfil/perfilAjax",
				type : "GET",
				dataType : "json",
				data : {
					max : idMax,
					idPerfil : perfil,
				}, //fi data
				success : function(publicacion) {
					$('#publicacions').empty();
					$.each(publicacion, function() {
						var id = this['pk'];
						var dataHora = this['fields']['dataHora'];
						var text = this['fields']['text'];
						var privat = this['fields']['privat'];

						$('#publicacions').append(
						'<div class="col-md-12">' +
						'<div class="panel panel-primary">' + 
						'<div class="panel-heading">' + dataHora + '</div>' + 
						'<div class="panel-body">' + text + 
						'</div>' + 
						'<div class="panel-footer">' +
						'<button class="btn btn-info" onclick="Comentar(' + id + ')" data-target="#coment" data-toggle="modal">' +
						'<span class="glyphicon glyphicon-edit"></span> Comenta</button><br/><br/>' +
						'</div>' +
						'</div>' +
						'</div>'
						);

					});
					document.getElementById('idMax').value = eval(idMax) + 5;
					//fi function
				}, //fi succes
				error : function(xhr, errmsg, err) {
					$('#buscar').append('<p>Error</p>');
				}
			});
			//fi ajax
			return false;
		}
	});
	//fi scroll

});
// fi ready
