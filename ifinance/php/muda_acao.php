<?php
    session_start();
    require_once("conexao.php");

    $_SESSION['verifica'] = 1;

    //BUSCANDO OS DADOS DO ATIVO
    $cod_acao = $_POST['cod_acao'];

    $result = $conexao->prepare("SELECT * FROM empresa  WHERE ativo = ? ORDER BY id_empresa DESC LIMIT 1");
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

    if (empty($_SESSION['ativo'])) {
      $_SESSION['verifica'] = 0;
    }

    header('Location:../index.php')
 ?>