$(document).ready (function(){
		$(window).scroll(function() {
		if ($(window).scrollTop() == $(document).height() - $(window).height()) {

			var com;
			//comentaris pasats ajax
			var perf;
			//perfils pasats ajax
			var domini = "http://127.0.0.1:8000";
			var mesos = ['gener', 'febrer', 'març', 'abril', 'maig', 'juny', 'juliol', 'agost', 'setembre', 'octubre', 'novembre', 'desembre'];

			//començar perfils

			$.ajax({
				url : domini + "/perfil/comentarisPerfil",
				dataType : "json",
				success : function(perfils) {
					perf = perfils;
					//fi function
				}, //fi succes
				error : function(xhr, errmsg, err) {
					$('#publicacions').append('<p>Error del servidor</p>');
				}
			});
			//fi ajax

			//finalitza perfils

			//començar comentaris
			$.ajax({
				url : domini + "/perfil/comentarisAjax",
				dataType : "json",
				success : function(comentaris) {
					com = comentaris;
					//fi function
				}, //fi succes
				error : function(xhr, errmsg, err) {
					$('#publicacions').append('<p>Error del servidor</p>');
				}
			});
			//fi ajax
			//finalitza comntaris

			var idMax = document.getElementById('idMax').value;

			$.ajax({
				url : domini + "/perfil/perfilTuAjax",
				type : "GET",
				dataType : "json",
				data : {
					max : idMax,
				}, //fi data
				success : function(publicacion) {
					$('#publicacions').empty();
					$.each(publicacion, function() {
						var id = this['pk'];
						var d = this['fields']['dataHora'];
						var text = this['fields']['text'];
						var usuari = this['fields']['usuari'];
						var privat = this['fields']['privat'];
						var imatge = this['fields']['imatge'];
						var priv;
						var dataHora = new Date(d);
						//alert(dataHora);
						
						if (privat == true) {
							priv = "Privada";
						}
						else {
							priv = "Pública";
						}

						var dh = dataHora.getDate() + ' de ' + mesos[dataHora.getMonth()] + ' de ' + dataHora.getFullYear() + ' a les ' + dataHora.getHours() + ":" + dataHora.getMinutes();
						
						if(imatge) {
							$('#publicacions').append('<div class="col-md-12">' + 
						'<div class="panel panel-primary">' + 
						'<div class="panel-heading">' + dh + ' <a href="/perfil/modificaPub/' + id + '" class="btn btn-info"><span class="glyphicon glyphicon-edit"></span> Edita</a>' +
						' -- ' + priv + ' <a href="/perfil/eliminaPub/' + id + '" class="btn btn-danger"><span class="glyphicon glyphicon-trash"></span></a>' +
						'</div>' + '<div class="panel-body"><p><a href="/media/' + imatge + '"><img class="img-responsive" src="/media/' + imatge + '" width="200px" height="200px" alt="Imatge publicacio" /></a></p><p align="justify">' + text + 
						'</p><a href="https://twitter.com/share" class="twitter-share-button" data-related="avaquero30" data-url="http://www.socialfootball.cat/perfil/publicacio/' + id + '" data-lang="ca" data-size="large">Tuiteja</a>' +
						'</div>' + '<div class="panel-footer" id="pub' + id + '">' + 
						'<button class="btn btn-info" onclick="Comentar(' + id + ')" data-target="#coment" data-toggle="modal">' + '<span class="glyphicon glyphicon-edit"></span> Comenta</button><br/><br/>' + '</div>' + 
						'</div>' + 
						'</div>');
						}
						else {
							$('#publicacions').append('<div class="col-md-12">' + 
						'<div class="panel panel-primary">' + 
						'<div class="panel-heading">' + dh + ' <a href="/perfil/modificaPub/' + id + '" class="btn btn-info"><span class="glyphicon glyphicon-edit"></span> Edita</a>' +
						' -- ' + priv + ' <a href="/perfil/eliminaPub/' + id + '" class="btn btn-danger"><span class="glyphicon glyphicon-trash"></span></a>' +
						'</div>' + '<div class="panel-body"><p align="justify">' + text + 
						'</p><a href="https://twitter.com/share" class="twitter-share-button" data-related="avaquero30" data-url="http://www.socialfootball.cat/perfil/publicacio/' + id + '" data-lang="ca" data-size="large">Tuiteja</a>' +
						'</div>' + '<div class="panel-footer" id="pub' + id + '">' + 
						'<button class="btn btn-info" onclick="Comentar(' + id + ')" data-target="#coment" data-toggle="modal">' + '<span class="glyphicon glyphicon-edit"></span> Comenta</button><br/><br/>' + '</div>' + 
						'</div>' + 
						'</div>');
						}
						

						$.each(com, function() {

							var comentari = this['fields']['comentari'];
							var pub = this['fields']['publicacio'];
							var user = this['fields']['usuari'];
							var hora = this['fields']['dataHora'];
							var dataHora = new Date(hora);
							var dh = dataHora.getDate() + ' de ' + mesos[dataHora.getMonth()] + ' de ' + dataHora.getFullYear() + ' a les ' + dataHora.getHours() + ":" + dataHora.getMinutes();

							if (pub == id) {
								$.each(perf, function() {

									var nom = this['fields']['nom'];
									var cognoms = this['fields']['cognoms'];
									var perfil = this['pk'];

									if (perfil == user) {
										$('#pub' + pub).append('<div class="panel panel-success">' + '<div class="panel-heading"><a href="/perfil/' + user + '"> ' + nom + ' ' + cognoms + '</a> - ' + dh + '</div>' + '<div class="panel-body">' + '<p aling="justify">' + comentari + '</p>' + '</div>' + '</div>');
									}
								});
								//per
							}// fi if pub == id
						});
						//com
					});
					// pub
					document.getElementById('idMax').value = eval(idMax) + 5;

					//fi function
				}, //fi succes
				error : function(xhr, errmsg, err) {
					$('#publicacions').append('<p>Error del servidor</p>');
				}
			});
			//fi ajax publicacions

			return false;
		}

	});
	//fi scroll

}); //fi ready
