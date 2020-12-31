/**
 * 读取本地Excel文件
 * @param {用户上传Blob文件} file 
 * @param {读取成功回调} callback 
 */
function readWorkbookFromLocalFile(file, callback) {
	var reader = new FileReader();
	reader.onload = function(e) {
		var data = e.target.result;
		var workbook = XLSX.read(data, {type: 'binary'});
		if(callback) callback(workbook);
	};
	reader.readAsBinaryString(file);
}


