<?php
session_start();
//Aqui chamamos o arquivo de conexao com o banco de dados
require_once("php/conexao.php");

//Definido tipo 1 para gráfico
if (empty($_SESSION['verifica'])) {
  $_SESSION['verifica'] = 1;
}

//Definido tipo 1 para gráfico
if (empty($_SESSION['grafico'])) {
  $_SESSION['grafico'] = 0;
}

$limit = 21;
$data1 = '';
$data2 = '';
$id_empresa = '';

//Definido a ação 1 que é AMZN
if (empty($_SESSION['id_empresa'])) {
 $_SESSION['id_empresa'] = 1;
}

if(isset($_SESSION['id_empresa'])){
  $id_empresa = $_SESSION['id_empresa'];
}

$result = $conexao->prepare("SELECT t.* FROM (SELECT * FROM acao WHERE id_empresa = ? ORDER BY id_acao DESC LIMIT 21) t ORDER BY t.id_acao ASC");
$result->execute([$id_empresa]);

while ($row = $result->fetch()) {
  $data1 = $data1 . '"'. $row['data_acao'].'",';
  $data2 = $data2 . '"'. $row['close_acao'] .'",';
}

    //Definido a ação 1 que é AMZN
if (empty($_SESSION['verifica'])) {
  $cod_acao = 'AMZN';

  $result = $conexao->prepare("SELECT * FROM empresa WHERE ativo = ? ORDER BY id_empresa DESC LIMIT 1");
  $result->execute([$cod_acao]); 
  $table_acao = $result->fetch();

  $ativo = $table_acao['ativo'];
  $nomeEmpresa = $table_acao['nomeEmpresa'];
  $id_empresa = $table_acao['id_empresa'];

          //BUSCANDO OS DADOS DE PREVISAO
  $result = $conexao->prepare("SELECT * FROM previsao WHERE id_empresa = ? ORDER BY id_previsao DESC LIMIT 1");
  $result->execute([$id_empresa]); 
  $table_previsao = $result->fetch();

  $media = $table_previsao['media'];
  $fechamento = $table_previsao['fechamento'];
  $tendencia = $table_previsao['tendencia'];

  $_SESSION['ativo'] = $ativo;
  $_SESSION['nomeEmpresa'] = $nomeEmpresa;
  $_SESSION['id_empresa'] = $id_empresa;
  $_SESSION['media'] = $media;
  $_SESSION['fechamento'] = $fechamento;
  $_SESSION['tendencia'] = $tendencia;
  $_SESSION['verifica'] = 1;
}
?>
<!doctype html>
<html lang="pt-br">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  <meta name="description" content="">
  <meta name="author" content="Mark Otto, Jacob Thornton, and Bootstrap contributors">
  <meta name="generator" content="Jekyll v4.1.1">
  <title>I-Finance</title>

  <link rel="canonical" href="https://getbootstrap.com/docs/4.5/examples/dashboard/">

  <!-- Bootstrap core CSS -->
  <link href="css/bootstrap.min.css" rel="stylesheet" integrity="sha384-JcKb8q3iqJ61gNV9KGb8thSsNjpSL0n8PARn9HuZOnIxN0hoP+VmmDGMN5t9UJ0Z" crossorigin="anonymous">


  <!-- Favicons -->
  <link rel="apple-touch-icon" href="/docs/4.5/assets/img/favicons/apple-touch-icon.png" sizes="180x180">
  <link rel="icon" href="/docs/4.5/assets/img/favicons/favicon-32x32.png" sizes="32x32" type="image/png">
  <link rel="icon" href="/docs/4.5/assets/img/favicons/favicon-16x16.png" sizes="16x16" type="image/png">
  <link rel="manifest" href="/docs/4.5/assets/img/favicons/manifest.json">
  <link rel="mask-icon" href="/docs/4.5/assets/img/favicons/safari-pinned-tab.svg" color="#563d7c">
  <link rel="icon" href="/docs/4.5/assets/img/favicons/favicon.ico">
  <meta name="msapplication-config" content="/docs/4.5/assets/img/favicons/browserconfig.xml">
  <meta name="theme-color" content="#563d7c">

  <style>
    .bd-placeholder-img {
      font-size: 1.125rem;
      text-anchor: middle;
      -webkit-user-select: none;
      -moz-user-select: none;
      -ms-user-select: none;
      user-select: none;
    }

    @media (min-width: 768px) {
      .bd-placeholder-img-lg {
        font-size: 3.5rem;
      }
    }
  </style>

  <!-- Custom styles for this template -->
  <link href="css/dashboard.css" rel="stylesheet">
  <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
  <link rel="stylesheet" href="css/keyboard.css">
</head>
<body class="p-3 mb-2 bg-dark text-white">
  <div class="container-fluid">
   <div class="row">
    <div class="col-3">
      <div class="card bg-dark text-white" style="width: 100%;">
        <div class="card-body">
          <h6 class="card-title">Pesquisar ativo</h6>
          <form method="POST" action="php/muda_acao.php">
           <div class="form-group">
            <input type="text" class="form-control use-keyboard-input" name="cod_acao" id="cod_acao">
          </div>
          <button type="submit" class="btn btn-success mb-2">Pesquisar</button>
        </form>
      </div>
    </div>
    <br>
    <br>
    <div class="card bg-dark text-white" style="width: 100%;">
      <div class="card-body">
        <a href="php/muda_grafico.php"><button type="button" class="btn btn-warning btn-lg btn-block">Tipo Gráfico</button></a>
      </div>
    </div>

  </div>
  <div class="col-9">
    <div class="card bg-dark text-white" style="width: 100%;">
      <div class="card-body">
        <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
          <div class="col-8">
            <h5 class="h5 text-uppercase">ATIVO: <?php echo $_SESSION['ativo']?></h5>
          </div>
          <div class="col-2 text-warning text-uppercase">
            TENDÊNCIA DE <?php echo $_SESSION['tendencia']?>
          </div>
        </div>
        <?php
        if (isset($_SESSION['ativo'])) {
              if ($_SESSION['grafico'] == 0) {
                ?> 
                <canvas class="my-4 w-100" id="myChart" width="800px" height="300px"></canvas></div>
                <?php
              }
              if ($_SESSION['grafico'] == 1) {
                ?>
                <canvas class="my-4 w-100" id="barChart" width="800px" height="300px"></canvas></div>
                <?php
              }
        }else{
              ?>
              <canvas width="800px" height="300px"></canvas><h2 class="text-center">Ativo não encontrado</h2></div>
              <?php
            }
            ?>
      </div>
    </div>  
  </div>
  <br>
  <div class="row text-center">
    <div class="col-sm">
      <div class="card bg-dark text-white" style="width: 100%;">
        <div class="card-body">
          <H4>I-FINANCE</H4>
          <p>O Software para Mercado Financeiro</p>
        </div>  
      </div>
    </div>

    <div class="col-sm">
      <div class="card bg-dark text-white" style="width: 100%;">
        <div class="card-body text-uppercase">
          <H4><?php echo $_SESSION['nomeEmpresa']?></H4>
          <br>
        </div>  
      </div>
    </div>

    <div class="col-sm">
      <div class="card bg-dark text-white" style="width: 100%;">
        <div class="card-body">
          <H4>PERÍODO GRÁFICO</H4>
          <b><p class="text-warning">Diário - 21 dias</p></b>
        </div>  
      </div>
    </div>

    <div class="col-sm">
      <div class="card bg-dark text-white" style="width: 100%;">
        <div class="card-body text-uppercase">
          <H4>PREVISÃO DE ENTRADA</H4>
          <b><p class="text-success">OPORTUNIDADE DE <?php  
          if ($_SESSION['tendencia'] == 'alta') {
            echo "compra";
          }

          if ($_SESSION['tendencia'] == 'baixa') {
            echo "venda";
          }
          ?></p></b>
        </div>  
      </div>
    </div>
  </div>              
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
  <script>window.jQuery || document.write('<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"><\/script>')</script><script src="js/bootstrap.bundle.min.js" integrity="sha384-LtrjvnR4Twt/qOuYxE721u19sVFLVSA4hf/rRt6PrZTmiPltdZcI7q7PXQBYTKyf" crossorigin="anonymous"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/feather-icons/4.9.0/feather.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.7.3/Chart.min.js"></script>
  <script src="js/keyboard.js"></script>
  <script>
    /* globals Chart:false, feather:false */

    (function () {
      'use strict'

      feather.replace()

                  // Graphs
                  var ctx = document.getElementById('myChart')
                  // eslint-disable-next-line no-unused-vars
                  var myChart = new Chart(ctx, {
                    type: 'line',
                    data: {
                      labels: [<?php echo $data1?>],
                      datasets: [{
                        data: [<?php echo $data2?>
                          ],
                          lineTension: 0,
                          backgroundColor: 'transparent',
                          borderColor: '#5cb85c',
                          borderWidth: 1,
                          pointBackgroundColor: '#5cb85c'
                        }]
                      },
                      options: {
                        scales: {
                          yAxes: [{
                            ticks: {
                              beginAtZero: false
                            }
                          }]
                        },
                        legend: {
                          display: false
                        }
                      }
                    })
                }())
              </script>
              <script>
           //bar
           var ctxB = document.getElementById("barChart").getContext('2d');
           var myBarChart = new Chart(ctxB, {
            type: 'bar',
            data: {
              labels: [<?php echo $data1?>],
              datasets: [{
                data: [<?php echo $data2?>],
                backgroundColor: '#5cb85c',
                borderColor: '#5cb85c',
                borderWidth: 1
              }]
            },
            options: {
              scales: {
                yAxes: [{
                  ticks: {
                    beginAtZero: false
                  }
                }]
              },
              legend: {
                display: false
              }
            }
          });
        </script>
      </body>
      </html>
