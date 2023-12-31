# 超啟發式演算法

> [!NOTE]
> HW1 ~ HWX 皆共用其父層的同一個 main function
> 

## :bookmark_tabs: 報告 ＆ 說明

<table>
<tr>
<th> 結果＆說明檔 </th>
<th> Command 通用指令 </th>
</tr>
<tr>
<td  width="50%">

#### :small_blue_diamond: &ensp; 總作業報告 :  [連結📎](https://omniscient-macaw-5c4.notion.site/HW-a03c22a7342a4d5ca41595d8362f4a29?pvs=4)
    
#### &ensp;&ensp;&ensp;&ensp;&ensp; ⌊ HW1報告 :   [連結📎](https://omniscient-macaw-5c4.notion.site/HW1-c9ddbc933a6c467392eb875659c10a73?pvs=4)
#### &ensp;&ensp;&ensp;&ensp;&ensp; ⌊ HW2報告 :   [連結📎](https://omniscient-macaw-5c4.notion.site/HW2-8780e6d91c8d480f84903e0d9b4de767?pvs=4)
#### &ensp;&ensp;&ensp;&ensp;&ensp; ⌊ HW3報告 :   [連結📎](https://omniscient-macaw-5c4.notion.site/HW3-49f20312579843b1b4a3834832f3bfbc?pvs=4)
#### &ensp;&ensp;&ensp;&ensp;&ensp; ⌊ HW4報告 :   [連結📎](https://omniscient-macaw-5c4.notion.site/HW4-a094c90f904644e89a3c556d1750fae2)
#### &ensp;&ensp;&ensp;&ensp;&ensp; ⌊ HW5報告 :   [連結📎](https://omniscient-macaw-5c4.notion.site/HW5-221ced3437084317bd6ab256eb129c21?pvs=4)
#### &ensp;&ensp;&ensp;&ensp;&ensp; ⌊ HW6報告 :   [連結📎](https://omniscient-macaw-5c4.notion.site/HW6-c918b05cca6342c6a33e831b3aa0d915?pvs=4)
#### &ensp;&ensp;&ensp;&ensp;&ensp; ⌊ HW7報告 :   [連結📎](https://omniscient-macaw-5c4.notion.site/HW7-d03682fdafdb4a63bf2133f1c3240593?pvs=4)
<br/>
</td>
<td  width="50%" style="background:#fff">
<img src="https://github.com/lanac0911/Hyper-Heuristic-Algo/blob/main/img/format.png" width="auto"/>
<img src="https://github.com/lanac0911/Hyper-Heuristic-Algo/blob/main/img/alogs.png"  width="auto" height="100"  />

```python
# Hill Climbing 做51回，每回100次，長度設100
    python3 main.py HC 51 100 100
# Simulated Annealing 「預設」做51回，每回100次，長度設100
    python3 main.py SA

⚠️ ACO & PSO 不適用 {bits len / n} 設定
```
 

</td>
</table>

## :bar_chart: 總表
|              	|            **演算法**           	|            **問題**           	|        **Code**       	|            **收斂圖**           	
|:--------------------:	|:---------------------------------:	|:---------------------------------:	|:---------------------------------:	|:---------------------------------:	
|     **HW1**     	| Exhaustive Search 	| One Max Problem 	| [📎](https://github.com/lanac0911/Hyper-Heuristic-Algo/tree/main/HW1)	| <img src="https://github.com/lanac0911/Hyper-Heuristic-Algo/blob/main/img/HW1.png" width="auto" height="250" />	| 
|     **HW2**    	| Hill Climbing 	| One Max Problem 	| [📎](https://github.com/lanac0911/Hyper-Heuristic-Algo/tree/main/HW2)	| <img src="https://github.com/lanac0911/Hyper-Heuristic-Algo/blob/main/img/HW2.png" width="auto" height="250" />	| 	
|  **HW3** 	| Simulated Annealing 	| One Max Problem、 Deceptive Problem| [📎](https://github.com/lanac0911/Hyper-Heuristic-Algo/tree/main/HW3)	| <img src="https://github.com/lanac0911/Hyper-Heuristic-Algo/blob/main/img/HW3-oneMax.png" width="auto" height="250" /> <img src="https://github.com/lanac0911/Hyper-Heuristic-Algo/blob/main/img/HW3-dece.png" width="auto" height="250" />	</br> (n=4)	| 	
|   **HW4**   	| Tabu Search 	| One Max Problem、 Deceptive Problem 	| [📎](https://github.com/lanac0911/Hyper-Heuristic-Algo/tree/main/HW4)		| <img src="https://github.com/lanac0911/Hyper-Heuristic-Algo/blob/main/img/HW4-oneMax.png" width="auto" height="250" /> <img src="https://github.com/lanac0911/Hyper-Heuristic-Algo/blob/main/img/HW4-deceN10.png" width="auto" height="250" /> </br> (n=10)	| 	
|      **HW5**      	|  Genetic Algorithm	|  One Max Problem	| [📎](https://github.com/lanac0911/Hyper-Heuristic-Algo/tree/main/HW5)	|  <img src="https://github.com/lanac0911/Hyper-Heuristic-Algo/blob/main/img/HW5.png" width="auto" height="250" />	| 	
|     **HW6**    	| Ant Colony Optimization	| Traveling Salesman Problem |  [📎](https://github.com/lanac0911/Hyper-Heuristic-Algo/tree/main/HW6)	| <img src="https://github.com/lanac0911/Hyper-Heuristic-Algo/blob/main/img/HW6.png" width="auto" height="250" /> 	|  	
|     **HW7**    	| Particle Swarm Optimiaztion |  Ackley Function |   [📎](https://github.com/lanac0911/Hyper-Heuristic-Algo/tree/main/HW7)	|  <img src="https://github.com/lanac0911/Hyper-Heuristic-Algo/blob/main/img/HW7-50.png" width="auto" height="250" /> 	<img src="https://github.com/lanac0911/Hyper-Heuristic-Algo/blob/main/img/HW7-10.png" width="auto" height="250" />  </br>(n=粒子數) | 

