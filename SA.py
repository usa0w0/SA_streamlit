from random import random, randint
import matplotlib.pyplot as plt
from math import sqrt, exp, log
from copy import deepcopy
import streamlit as st

# global parameter
field_x_range = 10
field_y_range = 10

temp_init = 300
temp_fin = 0.01
cooling_rate = 0.98
n_iteration = 20

plot_margin = field_x_range // 20
    
class SA:
    def __init__(self, n):
        self.n_city = n

        self.city_x_list = [random() * field_x_range for _ in range(self.n_city)]
        self.city_y_list = [random() * field_y_range for _ in range(self.n_city)]

        self.dist_log = []

        self.fig = plt.figure(figsize=(10, 5))
        self.plot_path()
        self.plot_path(index=2)
        self.plot_distLog()
        self.plot = st.pyplot(plt)

    def search_path(self):
        # init
        path_before = list(range(self.n_city))
        dist_before = self.calc_distance(path_before)
        self.dist_log.append(dist_before)

        temp = temp_init
        
        # while temp > temp_fin:
        for t_iter in range(int(log(temp_init/temp_fin, 1/cooling_rate))):

            for iteration in range(n_iteration):

                path_new = deepcopy(path_before)

                i = randint(0, self.n_city-2)
                j = randint(i+1, self.n_city-1)

                for k in range(i, j+1):
                    path_new[k] = path_before[i+j-k]
                
                dist_new = self.calc_distance(path_new)
                if dist_new < dist_before:
                    improve = True 
                else:
                    x = random()
                    improve = x < exp(-(dist_new-dist_before) / temp)

                if improve:
                    path_before = path_new 
                    dist_before = dist_new
                
                self.dist_log.append(dist_before)
            
            temp *= cooling_rate

            if t_iter % 10 == 0:
                self.plot_path(path_before, index=2)
                self.plot_distLog()
                self.plot.pyplot(plt)
        
        self.plot_path(path_before, index=2)
        self.plot_distLog()
        self.plot.pyplot(plt)

    def calc_distance(self, path):
        total = 0

        for i in range(self.n_city-1):
            dx = abs(self.city_x_list[path[i]] - self.city_x_list[path[i+1]])
            dy = abs(self.city_y_list[path[i]] - self.city_y_list[path[i+1]])
            total += sqrt(dx**2 + dy**2)

        return total

    def plot_path(self, path=False, index=1):
        if path:
            path_x = []
            path_y = []
            for i in path:
                path_x.append(self.city_x_list[i])
                path_y.append(self.city_y_list[i])

        ax = self.fig.add_subplot(1, 3, index)
        ax.set_xlim(-plot_margin, field_x_range + plot_margin)
        ax.set_ylim(-plot_margin, field_y_range+ plot_margin)
        ax.set_aspect(1.0)
        
        if path:
            ax.plot(path_x, path_y, c="gray")
            ax.scatter(self.city_x_list, self.city_y_list, c=path)
        else:
            ax.scatter(self.city_x_list, self.city_y_list)

    def plot_distLog(self):
        ax = self.fig.add_subplot(1, 3, 3)
        ax.set_ylim(self.n_city, self.n_city * 7)
        ax.tick_params(labelbottom=False, bottom=False)
        ax.plot(self.dist_log, c="gray")

def change_global(input_temp_init, input_temp_fin, input_cooling_rate, input_n_iteration):
    global temp_init, temp_fin, cooling_rate, n_iteration
    temp_init = input_temp_init
    temp_fin  = input_temp_fin
    cooling_rate = input_cooling_rate
    n_iteration  = input_n_iteration


if __name__ == "__main__":
    st.header('Simulated Annealing')
    n = st.number_input("生成するスポット数を入力してください", value=None, placeholder="Type a number...", min_value=2, step=1)

    input_temp_init = st.slider('初期温度', min_value=50, max_value=500, value=300)
    input_temp_fin  = st.slider('終了温度', min_value=0.0, max_value=1.0, value=0.01)
    input_cooling_rate = st.slider('冷却度', min_value=0.0, max_value=1.0, value=0.9)
    input_n_iteration = st.slider('繰り返し回数', min_value=1, max_value=500, value=200)
    change_global(input_temp_init, input_temp_fin, input_cooling_rate, input_n_iteration)

    if st.button('start'):
        if n != None:
            a = SA(n)
            a.search_path()
        else:
            st.warning('半角で入力してください')
    else:
        pass