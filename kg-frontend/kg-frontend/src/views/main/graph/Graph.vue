<template>
  <div class="graph">
    <div ref="chart" class="chart" v-loading="loading"></div>
    <div class="settings" style="color: #fff">
      <div class="header">
        <span class="el-icon-s-tools"></span>
        <span>&nbsp;图谱设置</span>
      </div>
      <div class="line">————————————</div>
      <div class="interval">
        <span class="text1">自动更新间隔</span>
        <div class="interval_time">300000</div>
        <div class="text2">上次更新时间 :</div>
        <div class="text3">{{ log.update_time }}</div>
        <div class="text2">更新问答对数量 :{{ log.qa_count }}</div>
        <div class="text2">更新节点数量 :{{ log.vertices_count }}</div>
      </div>
      <div class="toolbox">
        <div class="toolbox_content">
          <div class="toolbox_item">
            <span class="el-icon-refresh" @click="refresh"
              >&nbsp;&nbsp;刷新</span
            >
          </div>
          <div class="toolbox_item">
            <span class="el-icon-download" @click="toImage"
              >&nbsp;&nbsp;导出图片</span
            >
          </div>
          <div class="toolbox_item">
            <span class="el-icon-download" @click="toData"
              >&nbsp;&nbsp;导出数据</span
            >
          </div>
          <div class="toolbox_item">
            <span class="el-icon-download" @click="toLog"
              >&nbsp;&nbsp;导出日志</span
            >
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import * as echarts from "echarts";
import { getGraphData, getLog, getAllLog } from "@/api/graph";
import html2canvas from "html2canvas";
var chart = null;
export default {
  name: "Graph",
  components: {},
  data() {
    return {
      graphData: {},
      entity_types: [],
      colorList: ["#04f2a7", "#82dffe", "#fac858", "#ee6666", "#73c0de"],
      option: {},
      loading: true,
      timer: null,
      log: {},
    };
  },
  methods: {
    initGraph() {
      this.option = {
        legend: [
          {
            data: this.entity_types,
            itemWidth: 14,
            itemHeight: 14,
            itemGap: 10,
            top: "top",
          },
        ],
        series: [
          {
            type: "graph",
            layout: "force",
            label: {
              show: true,
              formatter: "{b}",
            },
            animation: false,
            large: true,
            largeThreshold: 1000,
            symbolSize: 20,
            edgeSymbol: ["none", "arrow"],
            edgeLabel: {
              show: true,
              formatter: "{c}",
              fontSize: 15,
              color: "#222222",
            },
            roam: true,
            draggable: true,
            data: this.graphData.Vertices.map((vertice) => {
              return {
                id: vertice.id.toString(),
                name: vertice.properties.name,
                category:
                  this.entity_types.indexOf(vertice.entity_type) != -1
                    ? this.entity_types.indexOf(vertice.entity_type)
                    : 4,
              };
            }),
            links: this.graphData.Edges.map((edge) => {
              return {
                source: edge.start_id.toString(),
                target: edge.target_id.toString(),
                value: edge.relationship_type,
              };
            }),
            categories: this.entity_types.map((item) => {
              return {
                name: item,
                itemStyle: {
                  borderColor:
                    this.colorList[
                      this.entity_types.indexOf(item) != -1
                        ? this.entity_types.indexOf(item)
                        : 4
                    ],
                  borderWidth: 2,
                  shadowBlur: 20,
                  shadowColor:
                    this.colorList[
                      this.entity_types.indexOf(item) != -1
                        ? this.entity_types.indexOf(item)
                        : 4
                    ],
                  color: "#001c43",
                },
              };
            }),
            force: {
              repulsion: 500,
              edgeLength: 80,
              layoutAnimation: true,
            },
          },
        ],
      };
      chart.setOption(this.option);
    },
    getGraphData() {
      getGraphData().then((res) => {
        this.graphData = res.data.data.graph;
        this.entity_types = res.data.data.mostCalledType.map((item) => item[0]);
        this.entity_types.push("other");
        localStorage.setItem("entity_types", JSON.stringify(this.entity_types));
        localStorage.setItem("graphData", JSON.stringify(this.graphData));
        this.loading = false;
        this.initGraph();
      });
    },
    refresh() {
      this.loading = true;
      this.getGraphData();
      this.getLog();
    },
    toImage() {
      const chartElement = this.$refs.chart; // 获取图表容器的 DOM 元素
      html2canvas(chartElement).then((canvas) => {
        const link = document.createElement("a");
        link.href = canvas.toDataURL("image/png"); // 将 Canvas 转换为图像数据 URL
        link.download = "chart.png"; // 下载文件的名称
        link.click();
      });
    },
    getLog() {
      getLog().then((res) => {
        this.log = res.data.data;
      });
    },
    toLog() {
      getAllLog().then((res) => {
        const data = res.data.data;
        let str = "";
        for (let i = 0; i < data.length; i++) {
          str +=
            "更新时间:" +
            data[i].update_time +
            "\n" +
            "更新问答对条数：" +
            data[i].qa_count +
            "\n" +
            "更新节点数和边数：" +
            data[i].vertices_count +
            " " +
            data[i].edges_count +
            "\n\n";
        }
        const blob = new Blob([str], { type: "text/plain" });
        const url = URL.createObjectURL(blob);

        const link = document.createElement("a");
        link.href = url;
        link.setAttribute("download", "log.txt");
        link.style.display = "none";
        document.body.appendChild(link);
        link.click();

        URL.revokeObjectURL(url);
        document.body.removeChild(link);
      });
    },
    toData() {
      const Graphdata = localStorage.getItem("graphData");
      const blob = new Blob([Graphdata], { type: "application/json" });
      const url = URL.createObjectURL(blob);

      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", "data.json");
      link.style.display = "none";
      document.body.appendChild(link);
      link.click();

      URL.revokeObjectURL(url);
      document.body.removeChild(link);
    },
  },
  created() {
    this.getLog();
  },
  mounted() {
    chart = echarts.init(this.$refs.chart);
    if (
      !localStorage.getItem("entity_types") ||
      !localStorage.getItem("graphData")
    ) {
      this.getGraphData();
    } else {
      this.entity_types = JSON.parse(localStorage.getItem("entity_types"));
      this.graphData = JSON.parse(localStorage.getItem("graphData"));
      this.loading = false;
      this.initGraph();
    }
    this.timer = setInterval(() => {
      this.refresh();
    }, 300000);
  },
  beforeDestroy() {
    clearInterval(this.timer);
    chart.clear();
  },
};
</script>
<style scoped>
.graph {
  /* background-color: aqua; */
  width: 105%;
  height: 95%;
  margin: 0 auto;
  border-radius: 20px;
  display: flex;
  border: 10px solid #e9e9e9;
}
.chart {
  width: 80%;
  height: 100%;
  transform: translateZ(0);
  will-change: transform;
}
.settings {
  background-color: #5aa4ae;
  width: 20%;
  height: 100%;
  border-bottom-right-radius: 10px;
  border-top-right-radius: 10px;
}
.header {
  font-size: 20px;
  margin-top: 30px;
  margin-bottom: 5px;
  text-align: center;
}
.line {
  text-align: center;
}
.interval {
  margin-top: 10px;
}
.text1 {
  margin-left: 20px;
}
.interval_time {
  margin-top: 15px;
  margin-bottom: 10px;
  font-size: 20px;
  width: 150px;
  height: 30px;
  background-color: #fff;
  color: #6e6e6e;
  line-height: 30px;
  margin-left: 22px;
  border-radius: 3px;
  padding-left: 10px;
}
.text2 {
  margin-left: 20px;
}
.text3 {
  padding-top: 5px;
  margin-left: 20px;
}
.toolbox {
  margin-top: 20px;
  /* text-align: center; */
  margin-left: 20px;
}
.toolbox .toolbox_content .toolbox_item {
  margin-top: 30px;
  font-size: 20px;
  cursor: pointer;
}
.refresh :hover {
}
</style>
