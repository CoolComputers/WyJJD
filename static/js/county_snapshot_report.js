
//remove county table header
var table_header_rows = $(".dataframe > thead > tr");
for(var i=0;i<table_header_rows.length;i++){
  if(table_header_rows[i].firstElementChild.textContent.includes("County")){
    $(table_header_rows[i]).addClass('d-none');
  }
}
