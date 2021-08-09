const file = document.querySelector('#file');
file.addEventListener('change', (e) => {
  const [file] = e.target.files;
  defaultImg.src = URL.createObjectURL(file)
  const { name: fileName, size } = file;
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
  document.querySelector("#file").removeAttribute('required');
  document.querySelector('.file-name').textContent = "";
}

