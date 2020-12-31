window.onload = function() {
    /**
     * 绑定执行聚类算法事件
     */
    document.getElementById("submit").addEventListener("click", function() {
        let file = document.getElementById("csv-loader").files[0];

        if(file == undefined) {
            alert("请选择聚类文件");
        } else {
            readWorkbookFromLocalFile(file, function(workbook) {
                /* 获取数据 */
                let sheetNames = workbook.SheetNames;
                let sheet = workbook.Sheets[sheetNames[0]];
                let csv = XLSX.utils.sheet_to_json(sheet);
                let data_frontEnd_qps = [], data_frontEnd_latency = []
                csv.forEach(function(row) {
                    data_frontEnd_qps.push(row["service/front-end/qps(2xx)"]*5)
                    data_frontEnd_latency.push(row["service/front-end/latency"]*5)
                });

                /* 获取用户设定超参数 */
                let clusteNum = document.getElementById("clusteNum").value
                let maxIterNum = document.getElementById("maxIterNum").value
                let data = {
                    qps: data_frontEnd_qps,
                    latency: data_frontEnd_latency
                };

                /* 清除原始图像 */
                document.getElementById("kmeans").innerHTML = "";

                /**
                 * 调用K-Means算法
                 * d3-figure, data, width, height, numPoints, numClusters, maxIter
                 */
                kMeans(
                    "#kmeans", 
                    data, csv.length, 
                    Math.max(...data_frontEnd_qps) + 100, Math.max(...data_frontEnd_latency) + 100,
                    parseInt(clusteNum), parseInt(maxIterNum)
                );
            });
        
        }
    });

    /**
     * 绑定取消事件
     */
    document.getElementById("clear").addEventListener("click", function() {
        document.getElementById("kmeans").innerHTML = "";
    });
};