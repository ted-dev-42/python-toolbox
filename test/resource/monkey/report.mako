<!DOCTYPE html>
<html lang="en">
<head>
    <meta name="Content-Type" content="text/html;charset=utf-8" />
    <title>Monkey Report</title>
    <style>
.pure-table {
    /* Remove spacing between table cells (from Normalize.css) */
    border-collapse: collapse;
    border-spacing: 0;
    empty-cells: show;
    border: 1px solid #cbcbcb;
    font-size: 0.8em;
}
.pure-table caption {
    color: #000;
    font: italic 85%/1 arial, sans-serif;
    padding: 1em 0;
    text-align: center;
}

.pure-table td,
.pure-table th {
    border-left: 1px solid #cbcbcb;/*  inner column border */
    border-bottom: 1px solid #cbcbcb;
    border-width: 0 0 1px 1px;
    font-size: inherit;
    margin: 0;
    overflow: visible; /*to make ths where the title is really long work*/
    padding: 0.5em 1em; /* cell padding */
    word-wrap: break-word;
    max-width: 450px;
}

.pure-table td:first-child,
.pure-table th:first-child {
    border-left-width: 0;
}

.pure-table thead {
    background-color: #e0e0e0;
    color: #000;
    text-align: left;
    vertical-align: bottom;
}

.pure-table td {
    background-color: transparent;
}
.pure-table-odd td {
    background-color: #f2f2f2;
}

/* nth-child selector for modern browsers */
.pure-table-striped tr:nth-child(2n-1) td {
    background-color: #f2f2f2;
}

.pure-table-bordered tbody > tr:last-child > td {
    border-bottom-width: 0;
}


/* HORIZONTAL BORDERED TABLES */

.pure-table-horizontal td,
.pure-table-horizontal th {
    border-width: 0 0 1px 0;
    border-bottom: 1px solid #cbcbcb;
}
.pure-table-horizontal tbody > tr:last-child > td {
    border-bottom-width: 0;
}
.bold {
    font-weight:bold;
}
.headline {
    font-size: 1.2em
}
    </style>
</head>
<body>
<br/>
<p class="headline bold">Monkey Test Result</p>
<span class="bold">Test Type: ${test_mode}</span>


%for result in result_list:
<table class="pure-table">
    <tr>
        <td>${packages()}</td>
        <td>${result.packages_str}</td>
    </tr>
    <tr>
        <td>Elapsed time</td>
        <td>${result.get_elapsed_time()}</td>
    </tr>
    <tr>
        <td>StopReason</td>
        <td>${result.stop_reason}</td>
    </tr>
    <tr>
        <td>First Abnormal Time</td>
        <td>${result.get_first_exception_time()}</td>
    </tr>
    <tr>
        <td>First ANR time</td>
        <td>${result.get_first_anr_time()}</td>
    </tr>
    <tr>
        <td>First Java Crash time</td>
        <td>${result.get_first_java_crash_time()}</td>
    </tr>
    <tr>
        <td>First Native Crash time</td>
        <td>${result.get_first_native_crash_time()}</td>
    </tr>
    <tr>
        <td>ANR(times)</td>
        <td> ${pkginfo(result.anr_packages)} </td>
    </tr>
    <tr>
        <td>Java Crash(times)</td>
        <td>${pkginfo(result.java_crash_packages)}</td>
    </tr>
    <tr>
        <td>Native Crash(times)</td>
        <td>${pkginfo(result.native_crash_packages)}</td>
    </tr>
</table>
<br/>
%endfor
</body>
<%def name="packages()">
    %if test_mode == 'white':
        Pakcage(includes)
    %elif test_mode == 'black':
        Package(excludes)
    %else:
        Package
    %endif
</%def>


<%def name="pkginfo(pkg_list)">
    %if len(pkg_list) > 0:
        %for pkg in pkg_list:
            ${pkg} : ${pkg_list[pkg]}
        %endfor
    %else:
        N/A
    %endif
</%def>
</html>

