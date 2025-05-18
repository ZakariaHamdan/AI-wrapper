using System.ComponentModel.DataAnnotations.Schema;
using RSG.Biovision.Domain.Entities.Interfaces;

namespace RSG.Biovision.Domain.Entities;

public class EmployeeSite : MainEntity , IHasCompany
{
    public Guid? EmployeeId { get; set; }
    public Guid SiteId { get; set; }
    public Guid CompanyId { get; set; }

    public Employee Employee { get; set; } = null!;
    public Site Site { get; set; } = null!;
}