<template>
<div>
<h5>Inline</h5>
<Calendar v-model="date14" :inline="true" :showWeek="true" />
</div>
</template>

<script>
export default {
    created() {
        let today = new Date();
        let month = today.getMonth();
        let year = today.getFullYear();
        let prevMonth = (month === 0) ? 11 : month -1;
        let prevYear = (prevMonth === 11) ? year - 1 : year;
        let nextMonth = (month === 11) ? 0 : month + 1;
        let nextYear = (nextMonth === 0) ? year + 1 : year;
        this.minDate = new Date();
        this.minDate.setMonth(prevMonth);
        this.minDate.setFullYear(prevYear);
        this.maxDate = new Date();
        this.maxDate.setMonth(nextMonth);
        this.maxDate.setFullYear(nextYear);

        let invalidDate = new Date();
        invalidDate.setDate(today.getDate() - 1);
        this.invalidDates = [today,invalidDate];
    },
    data() {
        return {
            date1: null,
            date2: null,
            date3: null,
            date4: null,
            date5: null,
            date6: null,
            date7: null,
            date8: null,
            date9: null,
            date10: null,
            date11: null,
            date12: null,
            date13: null,
            date14: null,
            dates1: null,
            dates2: null,
            es: {
                firstDayOfWeek: 1,
                dayNames: [ "Domingo","Lunes","Martes","Miércoles","Jueves","Viernes","Sábado" ],
                dayNamesShort: [ "Dom","Lun","Mar","Mié","Jue","Vie","Sáb" ],
                dayNamesMin: [ "D","L","M","X","J","V","S" ],
                monthNames: [ "Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre" ],
                monthNamesShort: [ "Ene","Feb","Mar","Abr","May","Jun","Jul","Ago","Sep","Oct","Nov","Dic" ],
                today: 'Hoy',
                clear: 'Borrar',
                weekHeader: 'Sm'
            },
            minDate: null,
            maxDate: null,
            invalidDates: null
        }
    }
}
</script>

<style>
.special-day {
    text-decoration: line-through;
}
</style>