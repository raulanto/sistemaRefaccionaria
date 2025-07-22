const path = require('path');
const BundleTracker = require('webpack-bundle-tracker');
const webpack = require('webpack');  // Asegúrate de requerir webpack
module.exports = {
    entry: {
        main: './static/src/main.js'
    },
    output: {
        path: path.resolve(__dirname, 'static/bundles/'),
        filename: '[name]-[hash].js',
        publicPath: '/static/bundles/',
    },
    plugins: [
        new BundleTracker({
            path: __dirname,  // Directorio base para el archivo de stats
            filename: 'webpack-stats.json',  // Solo el nombre del archivo (sin rutas)
        }),
        new webpack.ProvidePlugin({
            $: 'jquery',
            jQuery: 'jquery',
            Chart: 'chart.js/auto'
            // 'chart.js/auto' carga todos los componentes automáticamente
        })
    ],
    module: {
        rules: [
            {
                test: /\.js$/,
                exclude: /node_modules/,
                use: {
                    loader: 'babel-loader',
                    options: {
                        presets: ['@babel/preset-env'],
                    },
                },
            },
            {
                test: /\.css$/,
                use: ['style-loader', 'css-loader'],
            },
        ],
    },
    resolve: {
        modules: [
            path.resolve(__dirname, 'node_modules'),
            'node_modules'
        ],
        extensions: ['.js', '.json']
    }
};