$(document).ready(function()
  {
      $("#facet_box_1").hide();
      $("#facet_box_2").hide();
      $("#facet_box_3").hide();
      Dajaxice.search_engine.set_facet_search_type(Dajax.process);
      //Dajaxice.search_engine.updatecombo(Dajax.process,{'type_uri':'', 'prop_uri':'', 'value_uri':'', 'box':0, category:'start'});
      $('.chzn-select').chosen();
      $('#property_loader').hide()  // hide it initially
      $('#value_loader').hide()  // hide it initially
      $("#facet_search_type").change(function() {
    	  $('#property_loader').show();  
    	  $("#facet_rows_property_box").html("");
      });
      $("#intro_video").click(function() {
  	    alert("Introductory Video Coming Soon!")});
      
});

// clear text boxes on focus
$(function() {
    $('input[type=text]').focus(function() {
      $(this).val('');
      });
 });

// create loading wait boxes when search functions are called


		