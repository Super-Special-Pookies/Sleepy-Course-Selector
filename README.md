# Sleepy-Course-Selector

If you need sleep, so a scrapy helps you select course. 

**Note: This project is for reference only learn.**



## How-to use

```shell
python3 xk.py --xh MG20330000 --pw 12345678 --st 0.1
```



> xh: 学号
>
> pw: 密码
>
> st: 抢课间隙，做人留一地



右键选课检查，可以看到课程代码。

```python
bjdms = {
    "20201-033-081200D02-1592649131637" : "分布式算法入门",
    "20201-033-085401C02-1592649131522" : "信息技术前沿及行业应用",
    "20201-033-085401C01-1592649131579" : "分布式计算研究导引",
    "20201-4330-10284A001-1590476519355": "硕士生英语（硕士英语听力02）",
    "20201-033-085401D23-1594298344259" : "自然语言处理（自然语言处理）",
    "20201-033-085401D22-1592649131696" : "神经网络及其应用（神经网络及其应用）",
    "20201-033-085401D08-1592649131115" : "MapReduce海量数据并行处理（MapReduce海量数据并行处理）",
    "20201-033-081200D19-1590054822275" : "并发算法与理论（并发算法与理论）" 
}
```





## Requirements

```shell
pip install requests bs4 Pillow PyExecJS
```

