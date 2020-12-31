"use strict";

function kMeans(elt, data, numPoints, w, h, numClusters, maxIter) {
    var iter = 1,           // 当前迭代轮次
        centroids = [],     // 中心点集合
        points = [];        // 待聚类点集合
        
    var margin = {top: 30, right: 35, bottom: 20, left: 30},
        width = w - margin.left - margin.right,
        height = h - margin.top - margin.bottom;

    var colors = d3.scale.category20().range();
    
    var svg = d3.select(elt).append("svg")
        .style("width", width + margin.left + margin.right)
        .style("height", height + margin.top + margin.bottom);
        
    var group = svg.append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
    
    svg.append("g")
        .append("text")
        .attr("class", "label")
        .attr("transform", "translate(" + (width - margin.left - margin.right) + 
            "," + (height + margin.top + margin.bottom) + ")")
        .text("");

    /**
     * 欧拉坐标
     * @param {点1} a 
     * @param {点2} b 
     */
    function getEuclidianDistance(a, b) {
        var dx = b.x - a.x,
            dy = b.y - a.y;
        return Math.sqrt(Math.pow(dx, 2) + Math.pow(dy, 2));
    }
    
    
    let counter = -1;       // 获取数据点计数器
    /**
     * 获取数据集中下个点坐标
     * @param {该点的类型} type 
     * @param {该点的填充颜色} fill 
     */
    function getNextPoint(type, fill) {
        if(type !== "centroid") {
            counter++;
            return { 
                x: data.qps[counter],
                y: data.latency[counter],
                type: type,
                fill: fill 
            };
        } else {        // 初始中心点为数据集中的随机点
            return {
                x: data.qps[Math.floor(Math.round(Math.random() * width))],
                y: data.latency[Math.floor(Math.round(Math.random() * height))],
                type: type,
                fill: fill 
            };
        }
    }

    /**
     * 根据数据集初始化坐标点
     * @param {数据集中点的总数}} num 
     * @param {初始化时点的类型} type 
     */
    function initializePoints(num, type) {
        var result = [];
        for (var i = 0; i < num; i++) {
            var color = colors[i];
            if (type !== "centroid") {
                color = "#ccc";
            }
            var point = getNextPoint(type, color);
            point.id = point.type + "-" + i;
            result.push(point);
        }
        return result;
    }

    /**
     * 寻找距目标点最近的中心点
     * @param {目标点} point 
     */
    function findClosestCentroid(point) {
        var closest = {i: -1, distance: width * 2};
        centroids.forEach(function(d, i) {
            var distance = getEuclidianDistance(d, point);
            // 如果距离某个中心点更近则更新
            if (distance < closest.distance) {
                closest.i = i;
                closest.distance = distance;
            }
        });
        return (centroids[closest.i]); 
    }
    
    /**
     * 根据中心点颜色填充数据点颜色
     */
    function colorizePoints() {
        points.forEach(function(d) {
            var closest = findClosestCentroid(d);
            d.fill = closest.fill;
        });
    }

    /**
     * 更新中心点坐标 - 计算平均值
     * @param {聚类集群} cluster 
     */
    function computeClusterCenter(cluster) {
        return [
            d3.mean(cluster, function(d) { return d.x; }), 
            d3.mean(cluster, function(d) { return d.y; })
        ];
    }
    
    /**
     * 在集群中移动中心点
     */
    function moveCentroids() {
        centroids.forEach(function(d) {
            // 根据颜色提取集群中的点
            var cluster = points.filter(function(e) {
                return e.fill === d.fill;
            });
            // 重新计算中心点
            var center = computeClusterCenter(cluster);
            // 移动坐标
            d.x = center[0];
            d.y = center[1];
        });
    }

    /**
     * 更新图像
     */
    function update() {
        var data = points.concat(centroids);

        var circle = group.selectAll("circle")
            .data(data);
            
        // 创建新的点
        circle.enter().append("circle")
            .attr("id", function(d) { return d.id; })
            .attr("class", function(d) { return d.type; })
            .attr("r", 5);
            
        // 更新旧的点
        circle.transition().delay(100).duration(1000)
            .attr("cx", function(d) { return d.x; })
            .attr("cy", function(d) { return d.y; })
            .style("fill", function(d) { return d.fill; });
        
        // 删除旧点
        circle.exit().remove();
    }

    /**
     * 更新底部文字信息
     * @param {文字内容} text 
     */
    function setText(text) {
        svg.selectAll(".label").text(text);
    }
    
    /**
     * 执行算法的一轮迭代
     *  - 用距离最近中心的颜色填充改点颜色
     *  - 更新中心为集合的平均值
     */
    function iterate() {
        setText("Iteration " + iter + " of " + maxIter);

        colorizePoints();
        
        moveCentroids();
        
        update();
    }

    /** 
     * 初始化迭代算法 并 启动定时器
     */
    function initialize() {
        
        // 初始化数据集和中心点
        centroids = initializePoints(numClusters, "centroid");
        points = initializePoints(numPoints, "point");
        
        // 创建初始图像
        update();
        
        var interval = setInterval(function() {
            if(iter < maxIter + 1) {
                iterate();
                iter++;
            } else {
                clearInterval(interval);
                setText("Done");
            }
        }, 2 * 1000);
    }

    // 调用主函数
    initialize();
}