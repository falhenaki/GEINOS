/*** @jsx React.DOM */

    var products = []
for (var i = 0; i < data.length; i++) {
          var newprod = {
        name: data[i][0],
        role: data[i][1],
        email: "fake@fake.com",
        lastlogin: data[i][2]
      };
      products.push(newprod);
}
function onDeleteRow(rowKeys) {
  alert('You deleted: ' + rowKeys)
    const data = new FormData(event.target);
    fetch('/api/form-submit-url', {
      method: 'POST',
      body: data,
    });
}

const options = {
      afterDeleteRow: onDeleteRow
    }
function format(cell, row){
  return '<i class="glyphicon glyphicon-usd"></i> ' + cell;
}

var selectRowProp = {
  mode: "checkbox",
  clickToSelect: true,
};

ReactDOM.render(
<BootstrapTable data={products} selectRow={selectRowProp} options={options} condensed={true}  striped={true} hover={true} deleteRow pagination>
  <TableHeaderColumn dataField="name" isKey={true}  width="150"  dataSort>User Name</TableHeaderColumn>
  <TableHeaderColumn dataField="role"  width="150" >Role</TableHeaderColumn>
  <TableHeaderColumn dataField="email"  width="200" >Email</TableHeaderColumn>
  <TableHeaderColumn dataField="lastlogin"  width="150" dataSort >lastlogin</TableHeaderColumn>
</BootstrapTable>,

            document.getElementById("userTable")
    );