let nameOfFile="";

const file = document.querySelector('#file');
file.addEventListener('change', (e) => {
  const [file] = e.target.files;
  defaultImg.src = URL.createObjectURL(file)
  const { name: fileName, size } = file;
  nameOfFile=fileName;
  const fileSize = (size / 1000).toFixed(2);
  const fileNameAndSize = `${fileName} - ${fileSize}KB`;
  document.querySelector('.file-name').textContent = fileNameAndSize;
});

const samp1 = document.querySelector("#samp1");
samp1.onclick = function(){
  let mySrc = samp1.getAttribute('src');
  const defaultImg = document.querySelector("#defaultImg");
  const hiddenImg = document.querySelector("#hiddenImg");
  defaultImg.setAttribute ('src',mySrc);
  hiddenImg.setAttribute ('value','graph_def.png')
  if(nameOfFile==""){
    nameOfFile='graph_def.png';}
  document.querySelector("#file").removeAttribute('required');
  document.querySelector('.file-name').textContent = "";
}

const samp2 = document.querySelector("#samp2");
samp2.onclick = function(){
  let mySrc = samp2.getAttribute('src');
  const hiddenImg = document.querySelector("#hiddenImg");
  const defaultImg = document.querySelector("#defaultImg");
  defaultImg.setAttribute ('src',mySrc);
  hiddenImg.setAttribute ('value','graph_def2.png')
  if(nameOfFile==""){
    nameOfFile='graph_def2.png';}
  document.querySelector("#file").removeAttribute('required');
  document.querySelector('.file-name').textContent = "";
}

const samp3 = document.querySelector("#samp3");
samp3.onclick = function(){
  let mySrc = samp3.getAttribute('src');
  const hiddenImg = document.querySelector("#hiddenImg");
  const defaultImg = document.querySelector("#defaultImg");
  defaultImg.setAttribute ('src',mySrc);
  hiddenImg.setAttribute ('value','graph_def3.png')
  if(nameOfFile==""){
    nameOfFile='graph_def3.png';}
  document.querySelector("#file").removeAttribute('required');
  document.querySelector('.file-name').textContent = "";
}

function processMatrix(matrix){
  console.log(JSON.stringify(matrix));
  nodeArray = matrix.node_names;
  for(let i=0;i<matrix.num_nodes;++i)
    console.log(nodeArray[i]);
  let area = document.getElementById("analysis");
  let string = '<h2>Adjacency Matrix</h2><table><tr><th>Nodes</th>';
  for(let i=0;i<matrix.num_nodes;++i)
    string += '<th>'+nodeArray[i]+'</th>';
  string += '</tr>';
  for(let i=0;i<matrix.num_nodes;++i){
    string += '<tr><td>'+nodeArray[i]+'</td>';
    for(let j=0;j<matrix.num_nodes;++j){
       string += '<td>'+matrix.matrix[i][j]+'</td>';
    }
    string += '</tr>';
  } string += '</table><h2>Adjacency List</h2>'
  
  area.innerHTML = string;
}

function getMatrix(parameter){
  if(parameter!='none')
    {nameOfFile=parameter;
    console.log(parameter);
    }
  fetch('/matrix/'+nameOfFile)
  .then(function (response) {
    return response.json();
  })
  .then(function (text) {
    processMatrix(text); 
});
}