/*** @jsx React.DOM */

    var products = []
for (var i = 0; i < data.length; i++) {
          var newprod = {
        model: data[i][1],
        sn: data[i][0]
          };
      products.push(newprod);
}


function format(cell, row){
  return '<i class="glyphicon glyphicon-usd"></i> ' + cell;
}


var selectRowProp = {
  mode: "checkbox",
  clickToSelect: true,
};


ReactDOM.render(

    <BootstrapTable data={products} selectRow={selectRowProp} condensed striped={true} hover={true}
                    deleteRow pagination>
        <TableHeaderColumn dataField="model" width="150" dataSort>Model</TableHeaderColumn>
        <TableHeaderColumn dataField="sn" width="150" isKey dataSort>Serial Number</TableHeaderColumn>
    </BootstrapTable>,
        document.getElementById("devTable")
)

