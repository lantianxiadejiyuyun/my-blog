// 深色/浅色模式切换，状态持久化到 localStorage
import { ref, watchEffect } from 'vue'

const isDark = ref(localStorage.getItem('theme') === 'dark')

watchEffect(() => {
  document.documentElement.classList.toggle('dark', isDark.value)
  localStorage.setItem('theme', isDark.value ? 'dark' : 'light')
})

export function useTheme() {
  const toggle = () => { isDark.value = !isDark.value }
  return { isDark, toggle }
}
