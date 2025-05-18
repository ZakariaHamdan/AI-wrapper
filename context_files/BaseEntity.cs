using System;
using BuildingBlock.Core.Domain.Interfaces;

namespace BuildingBlock.Core.Domain.Abstractions;

public abstract class AuditedEntity<TKey> : BaseEntity<TKey>, IAudit, ISoftDelete
{
    public string Creator { get; set; } = "Anonymous";


    public DateTime CreationTime { get; set; }

    public string? LastModifier { get; set; }

    public DateTime? LastModificationTime { get; set; }

    public string? Deleter { get; set; }

    public DateTime? DeletionTime { get; set; }

    public bool IsDeleted { get; set; }
}