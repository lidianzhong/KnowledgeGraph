const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
    transpileDependencies: true,

    devServer: {
        historyApiFallback: true,
        allowedHosts: "all",
    },
})
module.exports = {
    configureWebpack: {
        resolve: {
            alias: {
                'assets': '@/assets',
                'common': '@/common',
                'components': '@/components',
                'api': '@/api',
                'views': '@/views',
            }
        }
    },
    devServer: {
        historyApiFallback: true,
        allowedHosts: "all",
    },
}
