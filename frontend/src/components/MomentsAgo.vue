<template>
  <span
    v-if="date"
    class="vue-moments-ago"
  >{{ prefix }} {{ humanDifference | plural(humanWord, lang) }} {{suffix}}</span>
</template>

<script>
import Vue from "vue";
import moment from "moment";
Vue.prototype.moment = moment;

export default {
  data() {
    return {
      epochs: ["year", "month", "day", "hour", "minute"],
      epochs_br: ["ano", "mês", "dia", "hora", "minuto"],
      year: 31536000,
      month: 2592000,
      day: 86400,
      hour: 3600,
      minute: 60,
      humanReadable: "",
      humanDifference: 0,
      humanWord: "momento"
    };
  },

  props: {
    prefix: {
      type: String,
      default: "há"
    },
    suffix: {
      type: String,
      default: "atrás"
    },
    date: {
      type: String,
      required: true
    },
    lang: {
      type: String,
      default: "br"
    }
  },

  mounted() {
    setInterval(() => {
      this.getSeconds(this.date);
    }, 1000);
  },

  filters: {
    plural(value, name, lang) {
      let plural;
      if (value === 0) {
        if (lang == "br") {
          return " alguns " + name + "s";
        } else {
          return " alguns " + name + "s";
        }
      } else if (value > 1) {
        if (lang == "en") {
          return value + " " + name + "s";
        } else if (lang == "br") {
          return value + " " + name + "s"
        } else {
          return value + " " + name + "";
        }
      } else {
        return value + " " + name;
      }
    }
  },

  methods: {
    getSeconds(time) {
      let seconds = moment().diff(moment(time), "seconds");
      this.humanReadable = this.getDuration(seconds);
      if (this.humanReadable) {
        this.humanDifference = this.humanReadable.interval;
        this.humanWord = this.humanReadable.humanEpoch;
      }
    },
    getDuration(seconds) {
      let epoch, interval;
      let humanEpoch;
      for (let i = 0; i < this.epochs.length; i++) {
        epoch = this.epochs[i];
        if (this.lang == "br") {
          humanEpoch = this.epochs_br[i];
        } else {
          humanEpoch = this.epochs[i];
        }
        interval = Math.floor(seconds / this[epoch]);
        if (interval >= 1) {
          return { interval: interval, humanEpoch: humanEpoch };
        }
      }
    }
  }
};
</script>

<style scoped>
.vue-moments-ago {
  font-size: 12px;
}
</style>