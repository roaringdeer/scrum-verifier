<template>
    <div>
        <Chart type="line" :data="chartData" :options="chartOptions" :key="chartKey"/>
    </div>
</template>

<script>
import useTasks from '../store/tasks'
import useProjects from '../store/projects'

export default {
    data() {
		return {
			chartKey: 0,
			chartOptions: {
				scales: {
					xAxes: [{
						type: 'time',
						time: {
							unit: 'days'
						}
					}],
					yAxes: [{
						ticks: {
							beginAtZero: true
						}
					}]
				}
			}
		}
	},
	async setup(){
		const {tasks} = useTasks()
		const {selectedProject} = useProjects()
		return{
			tasks,
			selectedProject
		}
	},
	computed: {
		chartData: function(){
			return {
				datasets: [
					{
						label: 'Added cost',
						borderColor: '#AD2828',
						fill: false,
						data: this.selectedProject.stats.chart_data.added
					},
					{
						label: 'Burned cost',
						borderColor: '#32A852',
						fill: false,
						data: this.selectedProject.stats.chart_data.burned
					},{
						label: 'Left points',
						borderColor: '#42A5F5',
						fill: false,
						data: this.selectedProject.stats.chart_data.current
					},
				]
			}
		}
	},
	methods:{
		
	}
}
</script>

<style>

</style>