function getSong(id){
 	$.getJSON('http://localhost:3000/payload.json', function(payload) {
           console.log('selected media!' + payload.iframe);
           $('.media-player').html(payload.iframe);
    });
 }

 function nextSong(){
 	$.getJSON('http://localhost:3000/payload.json', function(payload) {
           console.log('selected media!' + payload.iframe);
           $('.media-player').html(payload.iframe);
    });
 }

 function prevSong(){
 	$.getJSON('http://localhost:3000/payload.json', function(payload) {
           console.log('selected media!' + payload.iframe);
           $('.media-player').html(payload.iframe);
    });
 }

window.onload = function()
                {
                   $(".track").click(function(event){
                   		event.preventDefault();
					 	track = this;
					    getSong(track);
					})

                   $(".next-media").click(function(event){
                   		event.preventDefault();
					    nextSong();
					})

                   $(".prev-media").click(function(event){
                   		event.preventDefault();
					    prevSong();
					})

                };