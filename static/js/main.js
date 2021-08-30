let nameOfFile="";
var matrix2;
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

function minDistance(matrix,dist,sptSet){
  let min = 99999;
  let min_index = -1;
  for(let v=0;v<matrix.num_nodes;++v){
    if(sptSet[v]==false&&dist[v]<=min){
      min=dist[v];
      min_index=v;
    }
  }
  return min_index;
}

function djistra(matrix,start,end){
  let dist=new Array(matrix.num_nodes);
  let sptSet=new Array(matrix.num_nodes);
  for(let i=0;i<matrix.num_nodes;++i){
    dist[i]=99999;
    sptSet[i]=false;
  }
  dist[start]=0;
  for(let count=0;count<matrix.num_nodes-1;++count){
    let u=minDistance(matrix,dist,sptSet);
    sptSet[u]=true;
    for(let v=0;v<matrix.num_nodes;++v){
      if(!sptSet[v] && matrix.matrix[u][v]!=0 && dist[u]!=99999 && dist[u]+matrix.matrix[u][v]<dist[v]){
        dist[v]=dist[u]+matrix.matrix[u][v];
      }
    }
  }
  //for(let i=0;i<matrix.num_nodes;++i)
    //console.log(matrix.node_names[i]+' '+dist[i]);
  return dist[end];
}

function djistracaller(){
  let snode=document.getElementById("snode").value;
  let enode=document.getElementById("enode").value;
  for(let i=0;i<matrix2.num_nodes;++i){
    if(matrix2.node_names[i]==snode) snode=i;
    if(matrix2.node_names[i]==enode) enode=i;
  }
  console.log("Finding paths between "+snode+" "+enode);
  let ret = djistra(matrix2,snode,enode);
  let space=document.getElementById("mindistresult");
  string='<br>Shortest Path from '+matrix2.node_names[snode]+' to '+matrix2.node_names[enode]+' is '+ret+'<br>';
  space.innerHTML=string;

}

function processMatrix(matrix){
  //console.log(JSON.stringify(matrix));
  matrix2=matrix;
  nodeArray = matrix.node_names;
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
  } string += '</table><h2>Adjacency List</h2><div id="alist">'
  for(let i=0;i<matrix.num_nodes;++i){
    string += nodeArray[i]+' -> ';
    for(let j=0;j<matrix.num_nodes;++j){
      if(matrix.matrix[i][j]==1)
          string += nodeArray[j]+', ';
    }
    string += '<br>';
  }
  
  string+='</div><h2>Find shortest path between two Nodes using Djistras Algorithm:</h2>';
  string+='<br><div id="mindistance">'
  string+='<label for="snode">From Node:  </label>'
  string+='<input type="text" id="snode">'
  string+='<label for="enode">  to node:  </label>'
  string+='<input type="text" id="enode">'
  string+='<button id="mindistancebtn" onclick="djistracaller()">Find Path</button>';
  string+='</div><div id="mindistresult"></div>';
  area.innerHTML = string;
}

function getMatrix(parameter){
  if(parameter!='none')
    {nameOfFile=parameter;
    console.log(parameter);
    }
  if(nameOfFile=="") return;
  fetch('/matrix/'+nameOfFile)
  .then(function (response) {
    return response.json();
  })
  .then(function (text) {
    processMatrix(text); 
});
}

function pressButton(){
  document.getElementById("getJson").click();
}